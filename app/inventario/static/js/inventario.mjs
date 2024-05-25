function mostrarError(err) {
    const caja = document.getElementById("caja_errores")
    caja.innerText = err
    caja.classList.remove("hidden")
    setTimeout(() => {
        caja.classList.add("hidden")
    }, 10000);
}

/**
 * Mover un ataque de la columna de ataques a la columna de ataques equipados
 * @param {string} ataqueId 
 */
function ataqueColumnaEquipar(ataqueId) {
    const card = document.querySelector(`[desequipado-ataque-id="${ataqueId}"]`)
    const columnaEquipados = document.getElementById("columna_equipados")
    columnaEquipados.append(card)
    card.setAttribute("equipado-ataque-id", ataqueId)
    card.removeAttribute("desequipado-ataque-id")
}

/**
 * Mover un ataque de la columna de ataques equipados a la columna de ataques
 * @param {string} ataqueId
 */
function ataqueColumnaDesequipar(ataqueId) {
    const card = document.querySelector(`[equipado-ataque-id="${ataqueId}"]`)
    const columnaDesequipados = document.getElementById("columna_desequipados")
    columnaDesequipados.append(card)
    card.setAttribute("desequipado-ataque-id", ataqueId)
    card.removeAttribute("equipado-ataque-id")

}

/**
 * Equipar un ataque
 * @param {string} ataqueId 
 */
async function equipar(ataqueId) {
    const response = await fetch("/inventario/ataque", { headers: { "Content-Type": "application/json" }, method: "POST", body: JSON.stringify({ ataque_id: ataqueId }) })
    const data = await response.json()
    if (data.error) {
        mostrarError(data.error)
        return
    }
    ataqueColumnaEquipar(ataqueId)
    window.location.reload()
}

/**
 * Desequipar un ataque
 * @param {string} ataqueId 
 */
async function desequipar(ataqueId) {
    const response = await fetch("/inventario/ataque", { headers: { "Content-Type": "application/json" }, method: "DELETE", body: JSON.stringify({ ataque_id: ataqueId }) })
    const data = await response.json()
    if (data.error) {
        mostrarError(data.error)
        return
    }
    ataqueColumnaDesequipar(ataqueId)
    window.location.reload()
}

for (const btn of document.querySelectorAll("[equipar-ataque-id]")) {
    btn.addEventListener("click", async () => {
        const id = btn.getAttribute("equipar-ataque-id")
        equipar(id)
    })
}

for (const btn of document.querySelectorAll("[desequipar-ataque-id]")) {
    btn.addEventListener("click", async () => {
        const id = btn.getAttribute("desequipar-ataque-id")
        desequipar(id)
    })
}

// Drag and drop interaction
for (const card of document.querySelectorAll("[equipado-ataque-id]")) {
    card.addEventListener("dragstart", (event) => {
        event.dataTransfer.setData("ataqueId", card.getAttribute("equipado-ataque-id"))
    })
}

for (const card of document.querySelectorAll("[desequipado-ataque-id]")) {
    card.addEventListener("dragstart", (event) => {
        event.dataTransfer.setData("ataqueId", card.getAttribute("desequipado-ataque-id"))
    })
}

document.getElementById("columna_equipados").addEventListener("dragover", (event) => {
    event.preventDefault()
})

document.getElementById("columna_equipados").addEventListener("drop", async (event) => {
    event.preventDefault()
    const ataqueId = event.dataTransfer.getData("ataqueId")

    // Si está equipado no se vuelve a equipar
    if (document.querySelector(`[equipado-ataque-id="${ataqueId}"]`) != null) return

    const response = await fetch("/inventario/ataque", { headers: { "Content-Type": "application/json" }, method: "POST", body: JSON.stringify({ ataque_id: ataqueId }) })
    const data = await response.json()
    if (data.error) {
        mostrarError(data.error)
        return
    }
    ataqueColumnaEquipar(ataqueId)
    window.location.reload()
})


document.getElementById('columna_desequipados').addEventListener("dragover", (event) => {
    event.preventDefault()
})

document.getElementById('columna_desequipados').addEventListener("drop", async (event) => {
    event.preventDefault()
    const ataqueId = event.dataTransfer.getData("ataqueId")

    // Si no está equipado no se vuelve a desequipar
    if (document.querySelector(`[desequipado-ataque-id="${ataqueId}"]`) != null) return

    const response = await fetch("/inventario/ataque", { headers: { "Content-Type": "application/json" }, method: "DELETE", body: JSON.stringify({ ataque_id: ataqueId }) })
    const data = await response.json()
    if (data.error) {
        mostrarError(data.error)
        return
    }
    ataqueColumnaDesequipar(ataqueId)
    window.location.reload()
})