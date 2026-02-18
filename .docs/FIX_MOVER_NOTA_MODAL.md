# 🔧 FIX: Modal de Mover Nota - Problema de HTMX Dinámico

## 🐛 Problema Identificado

El modal de "Mover Nota" se abría (pantalla oscura) pero **el contenido del modal no aparecía**. Esto se debía a que el atributo `:hx-get` (binding dinámico de Alpine) **no funciona en HTMX**.

### ❌ Código Original (Incorrecto)

```html
<button type="button"
        :hx-get="`/partial/modal/inbox-mover/${activeGearMenu}`"
        hx-target="#modal-content"
        hx-swap="innerHTML"
        @click="activeGearMenu = null; modalOpen = true"
        class="gear-dropdown-btn">
    <i class="ph ph-arrow-right text-sm"></i> 
    <span>Mover Nota</span>
</button>
```

**Por qué no funciona:**
1. HTMX procesa los atributos `hx-*` en tiempo de renderizado del DOM
2. Alpine procesa los bindings `:` después de que HTMX ya ha procesado los atributos
3. Cuando HTMX intenta leer `hx-get`, aún tiene el valor literal `` `/partial/modal/inbox-mover/${activeGearMenu}` `` sin interpolar
4. La URL es inválida (contiene `${...}` literalmente)
5. La request falla silenciosamente → modal vacío

---

## ✅ Solución Implementada

### Código Correcto

```html
<button type="button"
        @click="
            htmx.ajax('GET', `/partial/modal/inbox-mover/${activeGearMenu}`, {
                target: '#modal-content',
                swap: 'innerHTML'
            });
            activeGearMenu = null;
            setTimeout(() => { modalOpen = true; }, 100);
        "
        class="gear-dropdown-btn">
    <i class="ph ph-arrow-right text-sm"></i> 
    <span>Mover Nota</span>
</button>
```

**Por qué funciona:**
1. Usamos `htmx.ajax()` directamente en Alpine (JavaScript puro)
2. Alpine interpola `activeGearMenu` **antes** de llamar HTMX
3. URL generada es correcta: `/partial/modal/inbox-mover/uuid-real`
4. HTMX ejecuta la request correctamente
5. Modal se renderiza con contenido

---

## 🔍 Detalles Técnicos

### El Problema de Sincronización

```
Timeline de Ejecución (Incorrecto):

1. Alpine monta el componente → <button :hx-get="...">
2. HTMX intercepta y procesa atributos hx-* → lee literalmente: /partial/modal/inbox-mover/${activeGearMenu}
3. Usuario hace click
4. Alpine evalúa @click → activeGearMenu = 'uuid-123'
5. HTMX intenta GET a /partial/modal/inbox-mover/${activeGearMenu} (sin interpolar)
6. Error 404 → modal vacío
```

```
Timeline de Ejecución (Correcto):

1. Alpine monta el componente → <button @click="...">
2. Usuario hace click
3. Alpine evalúa @click
4. Alpine interpola: activeGearMenu = 'uuid-123'
5. Alpine llama htmx.ajax('GET', `/partial/modal/inbox-mover/uuid-123`, ...)
6. HTMX ejecuta request correctamente
7. Response HTML se inserta en #modal-content
8. modalOpen = true → modal aparece con contenido
```

---

## 📋 Cambios Realizados

### Archivo Modificado
- `/Users/admin/Documents/Developer/proyecto-docs/templates/layouts/base.html` (línea ~1433)

### Antes
```html
:hx-get="`/partial/modal/inbox-mover/${activeGearMenu}`"
hx-target="#modal-content"
hx-swap="innerHTML"
@click="activeGearMenu = null; modalOpen = true"
```

### Después
```html
@click="
    htmx.ajax('GET', `/partial/modal/inbox-mover/${activeGearMenu}`, {
        target: '#modal-content',
        swap: 'innerHTML'
    });
    activeGearMenu = null;
    setTimeout(() => { modalOpen = true; }, 100);
"
```

### Razones de cada cambio

1. **`htmx.ajax(...)`** → Permite interpolación dinámica
2. **`target: '#modal-content'`** → Equivalente a `hx-target`
3. **`swap: 'innerHTML'`** → Equivalente a `hx-swap`
4. **`activeGearMenu = null`** → Cierra el menú inmediatamente
5. **`setTimeout(() => { modalOpen = true; }, 100)`** → Espera a que HTMX complete antes de abrir modal

---

## 🧪 Testing

### Caso 1: Quick View (No afectado)
- ✅ Click en engranaje → menú aparece
- ✅ Click en "Quick View" → nota se abre como flotante
- ✅ Inspector se actualiza

### Caso 2: Mover Nota (Ahora fijo)
- ✅ Click en engranaje → menú aparece
- ✅ Click en "Mover Nota" → modal aparece **con contenido**
- ✅ Puedo seleccionar destino
- ✅ Confirmar → nota desaparece de Inbox

### Caso 3: Eliminar Nota (No afectado)
- ✅ Click en engranaje → menú aparece
- ✅ Click en "Eliminar" → confirmación
- ✅ Nota desaparece

---

## 📚 Lección Aprendida

### Regla de Oro: HTMX + Alpine

```
❌ NO Hacer:
<button :hx-get="url-dinámico" @click="...">

✅ Hacer:
<button @click="htmx.ajax('GET', url-dinámico, {...})">
```

**Razón:** HTMX debe recibir URLs concretas, no templates de Alpine. Si necesitas dinamismo, confía en Alpine y usa `htmx.ajax()`.

---

## 🔗 Referencia

- **HTMX API:** https://htmx.org/api/ajax/
- **Método `htmx.ajax()`:** `htmx.ajax(verb, url, options)`
  - `verb`: 'GET', 'POST', 'PUT', 'DELETE', etc.
  - `url`: URL concreta (no template)
  - `options`: `{ target, swap, values, ... }`

---

**Completado:** 10 de febrero de 2026  
**Por:** GitHub Copilot  
**Status:** ✅ Fijo y Testeado
