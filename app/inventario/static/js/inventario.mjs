function mostrarError(err) {
    const caja = document.getElementById('caja_errores');
    caja.innerText = err;
    caja.classList.remove('hidden')
}

/**
 * Mover un ataque de la columna de ataques a la columna de ataques equipados
 * @param {string} ataqueId 
 */
function ataqueColumnaEquipar(ataqueId) {
    const card = document.querySelector(`[desequipado-ataque-id="${ataqueId}"]`);
    const columnaEquipados = document.getElementById('columna_equipados');
    columnaEquipados.append(card);
    card.setAttribute('equipado-ataque-id', ataqueId);
    card.removeAttribute('desequipado-ataque-id');
}

/**
 * Mover un ataque de la columna de ataques equipados a la columna de ataques
 * @param {string} ataqueId
 */
function ataqueColumnaDesequipar(ataqueId) {
    const card = document.querySelector(`[equipado-ataque-id="${ataqueId}"]`);
    const columnaDesequipados = document.getElementById('columna_desequipados');
    columnaDesequipados.append(card);
    card.setAttribute('desequipado-ataque-id', ataqueId);
    card.removeAttribute('equipado-ataque-id');

}

for (const btn of document.querySelectorAll('[equipar-ataque-id]')) {
    btn.addEventListener('click', async () => {
        const id = btn.getAttribute('equipar-ataque-id');
        const response = await fetch(`/inventario/ataque`, { headers: { 'Content-Type': 'application/json' }, method: 'POST', body: JSON.stringify({ ataque_id: id }) });
        const data = await response.json();
        if (data.error) {
            mostrarError(data.error);
            return
        }
        ataqueColumnaEquipar(id);
    });
}

for (const btn of document.querySelectorAll('[desequipar-ataque-id]')) {
    btn.addEventListener('click', async () => {
        const id = btn.getAttribute('desequipar-ataque-id');
        const response = await fetch(`/inventario/ataque`, { headers: { 'Content-Type': 'application/json' }, method: 'DELETE', body: JSON.stringify({ ataque_id: id }) });
        const data = await response.json();
        if (data.error) {
            mostrarError(data.error);
            return
        }
        ataqueColumnaDesequipar(id);
    });
}