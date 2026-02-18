# 🔧 Diagnóstico: Cómo mostrar el Modal

## El Flujo Actual

```
1. Usuario presiona engranaje
   └─ @htmx:before-request → aiLoading = true
   
2. HTMX hace petición GET
   
3. HTMX inserta HTML en #modal-content
   └─ @htmx:after-settle se ejecuta
   └─ Aquí se debería poner modalOpen = true
   
4. Alpine ve que modalOpen = true
   └─ x-show="modalOpen" → display: flex
   └─ Modal se muestra
```

## El Problema

**`modalOpen` no se está actualizando a `true`** después de que HTMX inserta el HTML.

Hemos probado:
- ❌ `@htmx:after-settle="modalOpen = true"` - No funciona
- ❌ Acceder directamente a _x_dataStack - Frágil
- ❌ Scripts en el modal - Se ejecutan pero no cambian estado

## ¿Por qué no funciona?

El evento `@htmx:after-settle` está en un botón que está dentro de `#contextual-sidebar`. Aunque el botón hereda el scope de Alpine desde `body[x-data]`, **cuando HTMX dispara el evento, Alpine podría no estar reaccionando**.

Esto se debe a que:
1. El evento HTMX se dispara
2. El listener `@htmx:after-settle` se ejecuta
3. **PERO Alpine no ve el cambio de `modalOpen`** porque el binding estábindose entre un elemento HTMX y Alpine

## La Solución Real

**Necesitamos un listener en el CONTENEDOR del modal** que detecte cuando HTMX ha insertado contenido ahí, y ENTONCES cambie `modalOpen = true`.

Es decir, el escuchador debe estar en o cerca de `#modal-content`, no en el botón.

Voy a mover el listener:
