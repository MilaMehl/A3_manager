import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from decimal import Decimal
from app.services.grouping_service import GroupingService


def _make_info_mock(id=1, classification="A", status="E", lat=-23.55, lon=-46.63):
    info = MagicMock()
    info.id = id
    info.latitude = Decimal(str(lat))
    info.longitude = Decimal(str(lon))
    info.classification = classification
    info.status = status
    info.created_at = datetime(2024, 6, 15)
    info.updated_at = datetime(2024, 6, 15)
    return info


def _make_request_mock(id=1, photo_path="public/images/foto.jpg"):
    r = MagicMock()
    r.id = id
    r.photo_path = photo_path
    r.to_dict = MagicMock(return_value={
        "id": id,
        "address": "Rua Teste, 100",
        "classification": "A",
        "status": "em andamento",
        "date": "2024-06-15T00:00:00",
        "latitude": -23.55,
        "longitude": -46.63,
    })
    return r


class TestGroupingServiceParsDate:
    def setup_method(self):
        self.service = GroupingService()

    def test_parse_date_formato_iso(self):
        result = self.service._parse_date("2024-06-15")
        assert result == datetime(2024, 6, 15)

    def test_parse_date_formato_datetime(self):
        result = self.service._parse_date("2024-06-15T10:30:00")
        assert result == datetime(2024, 6, 15, 10, 30, 0)

    def test_parse_date_formato_br(self):
        result = self.service._parse_date("15/06/2024")
        assert result == datetime(2024, 6, 15)

    def test_parse_date_none_retorna_none(self):
        assert self.service._parse_date(None) is None

    def test_parse_date_vazio_retorna_none(self):
        assert self.service._parse_date("") is None

    def test_parse_date_formato_invalido(self):
        with pytest.raises(ValueError, match="Formato de data inválido"):
            self.service._parse_date("15-06-2024")


class TestGroupingServiceBuildPhotoUrl:
    def setup_method(self):
        self.service = GroupingService()

    def test_build_photo_url_com_path(self, app):
        with app.test_request_context("/"):
            url = self.service._build_photo_url("public/images/foto.jpg")
            assert url is not None
            assert url.startswith("http")
            assert "public/images/foto.jpg" in url

    def test_build_photo_url_sem_path(self, app):
        with app.test_request_context("/"):
            assert self.service._build_photo_url(None) is None

    def test_build_photo_url_vazio(self, app):
        with app.test_request_context("/"):
            assert self.service._build_photo_url("") is None


class TestGroupingServiceSerialize:
    def setup_method(self):
        self.service = GroupingService()

    def test_serialize_retorna_campos_esperados(self, app):
        with app.test_request_context("/"):
            info = _make_info_mock()
            requests = [_make_request_mock()]
            result = self.service._serialize(info, requests)

            assert result["id"] == 1
            assert result["classification"] == "A"
            assert result["status"] == "E"
            assert isinstance(result["latitude"], float)
            assert isinstance(result["longitude"], float)
            assert result["total_requests"] == 1
            assert len(result["requests"]) == 1
            assert "created_at" in result
            assert "updated_at" in result

    def test_serialize_sem_campo_date(self, app):
        with app.test_request_context("/"):
            info = _make_info_mock()
            result = self.service._serialize(info, [])
            assert "date" not in result

    def test_serialize_request_inclui_photo_url(self, app):
        with app.test_request_context("/"):
            info = _make_info_mock()
            r = _make_request_mock(photo_path="img/foto.jpg")
            result = self.service._serialize(info, [r])
            assert "photo_url" in result["requests"][0]
            assert "img/foto.jpg" in result["requests"][0]["photo_url"]

    def test_serialize_request_photo_url_none_sem_foto(self, app):
        with app.test_request_context("/"):
            info = _make_info_mock()
            r = _make_request_mock(photo_path=None)
            result = self.service._serialize(info, [r])
            assert result["requests"][0]["photo_url"] is None


class TestGroupingServiceGetAllGroupings:
    def setup_method(self):
        self.service = GroupingService()

    @patch("app.services.grouping_service.grouping_repository")
    def test_retorna_lista_com_agrupamentos(self, mock_repo, app):
        info = _make_info_mock()
        mock_repo.find_all_with_requests.return_value = [info]
        mock_repo.find_requests_by_grouping_id.return_value = [_make_request_mock()]

        with app.test_request_context("/"):
            result = self.service.get_all_groupings()
            assert len(result) == 1
            assert result[0]["id"] == 1
            assert result[0]["total_requests"] == 1

    @patch("app.services.grouping_service.grouping_repository")
    def test_retorna_lista_vazia(self, mock_repo, app):
        mock_repo.find_all_with_requests.return_value = []

        with app.test_request_context("/"):
            result = self.service.get_all_groupings()
            assert result == []

    @patch("app.services.grouping_service.grouping_repository")
    def test_repassa_filtro_address(self, mock_repo, app):
        mock_repo.find_all_with_requests.return_value = []

        with app.test_request_context("/"):
            self.service.get_all_groupings(address="Paulista")
            mock_repo.find_all_with_requests.assert_called_once_with(
                address="Paulista",
                status=None,
                classification=None,
                date_from=None,
                date_to=None,
            )

    @patch("app.services.grouping_service.grouping_repository")
    def test_repassa_filtro_status_e_classification(self, mock_repo, app):
        mock_repo.find_all_with_requests.return_value = []

        with app.test_request_context("/"):
            self.service.get_all_groupings(status="E", classification="A")
            mock_repo.find_all_with_requests.assert_called_once_with(
                address=None,
                status="E",
                classification="A",
                date_from=None,
                date_to=None,
            )

    @patch("app.services.grouping_service.grouping_repository")
    def test_converte_e_repassa_datas(self, mock_repo, app):
        mock_repo.find_all_with_requests.return_value = []

        with app.test_request_context("/"):
            self.service.get_all_groupings(date_from="2024-01-01", date_to="2024-12-31")
            mock_repo.find_all_with_requests.assert_called_once_with(
                address=None,
                status=None,
                classification=None,
                date_from=datetime(2024, 1, 1),
                date_to=datetime(2024, 12, 31),
            )

    @patch("app.services.grouping_service.grouping_repository")
    def test_data_invalida_levanta_erro(self, mock_repo, app):
        with app.test_request_context("/"):
            with pytest.raises(ValueError, match="Formato de data inválido"):
                self.service.get_all_groupings(date_from="01-01-2024")

    @patch("app.services.grouping_service.grouping_repository")
    def test_multiplos_agrupamentos(self, mock_repo, app):
        infos = [_make_info_mock(id=1), _make_info_mock(id=2)]
        mock_repo.find_all_with_requests.return_value = infos
        mock_repo.find_requests_by_grouping_id.return_value = [_make_request_mock()]

        with app.test_request_context("/"):
            result = self.service.get_all_groupings()
            assert len(result) == 2
            assert result[0]["id"] == 1
            assert result[1]["id"] == 2
