import pytest
from unittest.mock import MagicMock, patch
from app.services.request_service import RequestService


def _make_request_mock(id=1, photo_path="public/images/foto.jpg"):
    r = MagicMock()
    r.id = id
    r.photo_path = photo_path
    r.to_dict = MagicMock(return_value={
        "id": id,
        "address": "Rua Teste, 100",
        "classification": "A",
        "status": "pending",
        "date": "2024-01-01",
        "latitude": -23.5,
        "longitude": -46.6,
    })
    return r


class TestRequestService:
    def setup_method(self):
        self.service = RequestService()

    def test_parse_date_formato_iso(self):
        from datetime import datetime
        result = self.service._parse_date("2024-06-15")
        assert result == datetime(2024, 6, 15)

    def test_parse_date_formato_datetime(self):
        from datetime import datetime
        result = self.service._parse_date("2024-06-15T10:30:00")
        assert result == datetime(2024, 6, 15, 10, 30, 0)

    def test_parse_date_formato_br(self):
        from datetime import datetime
        result = self.service._parse_date("15/06/2024")
        assert result == datetime(2024, 6, 15)

    def test_parse_date_none(self):
        assert self.service._parse_date(None) is None

    def test_parse_date_formato_invalido(self):
        with pytest.raises(ValueError, match="Formato de data inválido"):
            self.service._parse_date("15-06-2024")

    def test_build_photo_url_com_path(self, app, client):
        with app.test_request_context("/"):
            url = self.service._build_photo_url("public/images/foto.jpg")
            assert "public/images/foto.jpg" in url
            assert url.startswith("http")

    def test_build_photo_url_sem_path(self, app):
        with app.test_request_context("/"):
            url = self.service._build_photo_url(None)
            assert url is None

    @patch("app.services.request_service.request_repository")
    def test_get_filtered_retorna_lista(self, mock_repo, app):
        mock_repo.find_by_filters.return_value = [_make_request_mock()]
        with app.test_request_context("/"):
            result = self.service.get_filtered()
            assert isinstance(result, list)
            assert len(result) == 1
            assert "photo_url" in result[0]

    @patch("app.services.request_service.request_repository")
    def test_get_filtered_lista_vazia(self, mock_repo, app):
        mock_repo.find_by_filters.return_value = []
        with app.test_request_context("/"):
            result = self.service.get_filtered()
            assert result == []

    @patch("app.services.request_service.request_repository")
    def test_get_filtered_repassa_address(self, mock_repo, app):
        mock_repo.find_by_filters.return_value = []
        with app.test_request_context("/"):
            self.service.get_filtered(address="Paulista")
            mock_repo.find_by_filters.assert_called_once_with(
                date_from=None,
                date_to=None,
                status=None,
                classification=None,
                address="Paulista",
            )

    @patch("app.services.request_service.request_repository")
    def test_get_filtered_repassa_status_e_classification(self, mock_repo, app):
        mock_repo.find_by_filters.return_value = []
        with app.test_request_context("/"):
            self.service.get_filtered(status="em andamento", classification="buraco")
            mock_repo.find_by_filters.assert_called_once_with(
                date_from=None,
                date_to=None,
                status="em andamento",
                classification="buraco",
                address=None,
            )

    @patch("app.services.request_service.request_repository")
    def test_get_filtered_converte_datas(self, mock_repo, app):
        from datetime import datetime
        mock_repo.find_by_filters.return_value = []
        with app.test_request_context("/"):
            self.service.get_filtered(date_from="2024-01-01", date_to="2024-12-31")
            mock_repo.find_by_filters.assert_called_once_with(
                date_from=datetime(2024, 1, 1),
                date_to=datetime(2024, 12, 31),
                status=None,
                classification=None,
                address=None,
            )

    @patch("app.services.request_service.request_repository")
    def test_get_filtered_inclui_photo_url_no_resultado(self, mock_repo, app):
        mock_repo.find_by_filters.return_value = [_make_request_mock(photo_path="img/foto.jpg")]
        with app.test_request_context("/"):
            result = self.service.get_filtered()
            assert result[0]["photo_url"] is not None
            assert "img/foto.jpg" in result[0]["photo_url"]

    @patch("app.services.request_service.request_repository")
    def test_get_filtered_photo_url_none_quando_sem_foto(self, mock_repo, app):
        mock_repo.find_by_filters.return_value = [_make_request_mock(photo_path=None)]
        with app.test_request_context("/"):
            result = self.service.get_filtered()
            assert result[0]["photo_url"] is None
