// 1. Configuração Inicial e Travas de Limite
const limitesPedraBranca = [
    [-27.6380, -48.6980], // Sudoeste
    [-27.6100, -48.6650]  // Nordeste
];

const meuMapa = L.map('mapa', {
    center: [-27.6258, -48.6826],
    zoom: 16,
    minZoom: 15,
    maxZoom: 18,
    maxBounds: limitesPedraBranca,
    maxBoundsViscosity: 1.0 // Mapa "quica" de volta se tentar sair
});

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap'
}).addTo(meuMapa);

let camadaMarcadores = L.layerGroup().addTo(meuMapa);
let controleRota = null;

// 2. Ícones Personalizados
const linksIcones = {
    "Buraco na Via": "https://cdn-icons-png.flaticon.com/512/3595/3595537.png",
    "Poda de Árvore": "https://cdn-icons-png.flaticon.com/512/1518/1518915.png",
    "Árvore Caída": "https://cdn-icons-png.flaticon.com/512/3429/3429153.png",
    "Lixo Irregular": "https://cdn-icons-png.flaticon.com/512/1165/1165154.png",
    "Padrao": "https://cdn-icons-png.flaticon.com/512/684/684908.png"
};

// 3. Função para Renderizar Marcadores com Contorno
function renderizarMarcadores(lista) {
    camadaMarcadores.clearLayers();

    lista.forEach(function(chamado) {
        const iconeCustom = L.icon({
            iconUrl: linksIcones[chamado.tipo] || linksIcones["Padrao"],
            iconSize: [40, 40],
            iconAnchor: [20, 40],
            popupAnchor: [0, -40],
            className: `icone-${chamado.gravidade}` // Aplica o contorno do CSS
        });

        const marcador = L.marker([chamado.lat, chamado.lng], { icon: iconeCustom });

        const cores = { "leve": "#2ecc71", "moderada": "#f1c40f", "urgente": "#e74c3c" };
        const corBadge = cores[chamado.gravidade] || "#95a5a6";

        const conteudoPopup = `
            <div style="font-family: sans-serif; width: 250px;">
                <img src="${chamado.urlFoto}" style="width: 100%; height: 180px; object-fit: cover; border-radius: 8px; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <b style="font-size: 16px;">${chamado.tipo}</b>
                    <span style="padding: 2px 8px; border-radius: 4px; color: white; font-size: 10px; font-weight: bold; background: ${corBadge}; text-transform: uppercase;">
                        ${chamado.gravidade}
                    </span>
                </div>
                <p style="font-size: 13px; margin: 5px 0;">Por: <b>${chamado.usuario}</b></p>
                <p style="font-size: 12px; color: #7f8c8d;">${chamado.endereco}</p>
            </div>
        `;

        marcador.bindPopup(conteudoPopup);
        camadaMarcadores.addLayer(marcador);
    });
}

// Inicialização
renderizarMarcadores(chamadosMock);

// 4. Lógica de Filtros
document.querySelectorAll('.btn-filtro').forEach(botao => {
    botao.addEventListener('click', () => {
        document.querySelectorAll('.btn-filtro').forEach(b => b.classList.remove('ativo'));
        botao.classList.add('ativo');

        const categoria = botao.textContent;
        if (categoria === "Todos") {
            renderizarMarcadores(chamadosMock);
        } else {
            const termo = categoria.slice(0, -1).toLowerCase();
            const filtrados = chamadosMock.filter(c => c.tipo.toLowerCase().includes(termo));
            renderizarMarcadores(filtrados);
        }
    });
});

// 5. Lógica de Rota Otimizada
document.querySelector('.btn-rota').addEventListener('click', () => {
    if (controleRota) meuMapa.removeControl(controleRota);
    
    const pontos = [
        L.latLng(-27.6258, -48.6826), // Ponto da Empresa
        ...chamadosMock.map(c => L.latLng(c.lat, c.lng))
    ];

    controleRota = L.Routing.control({
        waypoints: pontos,
        lineOptions: { styles: [{ color: '#3498db', weight: 5 }] },
        createMarker: () => null,
        addWaypoints: false,
        routeWhileDragging: false
    }).addTo(meuMapa);
});