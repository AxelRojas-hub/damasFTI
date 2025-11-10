# Juego de Damas - Fundamentos Teóricos de la Informática

Un juego de damas implementado en Python que utiliza autómatas finitos para la validación de capturas y soporta todas las reglas clásicas del juego.

## Integrantes del Proyecto

- **Ana Botha**
- **Nadin González**
- **Axel Rojas**

## Características del Juego

- Tablero 8x8
- Validación automática
- Capturas múltiples
- Sistema de coronación

## Instalación y Ejecución

### 1. Clonar o Descargar el Proyecto

```bash
git clone [repositorio]
cd damasFTI
```

### 2. Instalar Dependencias

```bash
pip install automata-lib
```

### 3. Ejecutar el Juego

```bash
python damas.py
```

## Cómo Jugar

### Formato de Jugadas

Las jugadas se ingresan en el formato: `ColumnaOrigenFilaOrigen-ColumnaDestinoFilaDestino`

**Ejemplos:**

- `A3B4`: Mover ficha de A3 a B4
- `C5D6`: Mover ficha de C5 a D6
- `E4F5`: Mover ficha de E4 a F5

### Coordenadas del Tablero

```
    A   B   C   D   E   F   G   H
8 | · | ○ | · | ○ | · | ○ | · | ○ |
7 | ○ | · | ○ | · | ○ | · | ○ | · |
6 | · | ○ | · | ○ | · | ○ | · | ○ |
5 | · | · | · | · | · | · | · | · |
4 | · | · | · | · | · | · | · | · |
3 | ● | · | ● | · | ● | · | ● | · |
2 | · | ● | · | ● | · | ● | · | ● |
1 | ● | · | ● | · | ● | · | ● | · |
    A   B   C   D   E   F   G   H
```

### Representación de Fichas

- `○` / `n`: Fichas negras normales
- `●` / `b`: Fichas blancas normales
- `N`: Dama negra (coronada)
- `B`: Dama blanca (coronada)
- `·` / `-`: Casilla vacía

### Turnos

- Las **fichas blancas** siempre inician
- Los turnos se alternan automáticamente
- El juego indica qué color debe mover

## Reglas

2. **Las capturas múltiples se ejecutan automáticamente**
3. **Las piezas coronadas tienen libertad total de movimiento**
4. **El juego termina cuando un jugador no tiene fichas**
5. **La coronación es automática** al alcanzar la fila opuesta
