# Plan de Desarrollo Completo: Go-Chess Prototipo

## Requisitos Funcionales

### **Core del Juego**
- Tablero 8x8 inicialmente vacío
- Dos acciones: **Colocación** y **Movimiento**
- Validaciones Go-Chess:
  - No colocar piezas en jaque
  - Peones mínimo a 2 (o un número configurado de) casillas de coronación
  - Transición manual entre fases
  - Reglas configurables
- Reglas de ajedrez estándar en fase de movimiento
- Detección de jaque, jaque mate y tablas

### **Sistema de Configuración**
- Piezas permitidas por jugador (configurable)
- Límite de turnos para colocación (opcional)
- Distancia mínima de coronación (configurable)
- Presets de configuración predefinidos

### **Multijugador Local Básico**
- Códigos de sala de 6 dígitos
- Conexión por WebSocket
- Sincronización de movimientos en tiempo real
- Reconexión básica por código de sala

### **Requisitos No Funcionales**
- **Usabilidad**: Interfaz intuitiva, drag & drop opcional
- **Escalabilidad**: Arquitectura preparada para persistencia futura
- **Mantenibilidad**: Código modular y testeable
- **Simplicidad**: Evitar complejidades innecesarias en la fase inicial

## Arquitectura y Patrones

### **Arquitectura General**
```
┌─────────────────┐    WebSocket/HTTP    ┌─────────────────┐
│  React Frontend │ ←──────────────────→ │ FastAPI Backend │
│                 │                      │                 │
│ - UI Components │                      │ - API Endpoints │
│ - State Mgmt    │                      │ - WebSocket Hub │
│ - Game Display  │                      │ - Game Manager  │
└─────────────────┘                      └─────┬───────────┘
                                               │
                                         ┌─────▼───────────┐
                                         │ Chess Logic     │
                                         │ (Tu código)     │
                                         │                 │
                                         │ - GoChessEngine │
                                         │ - Validators    │
                                         │ - Game Rules    │
                                         └─────────────────┘
```

### **Patrones Arquitectónicos Clave**

#### **1. Hexagonal Architecture (Backend)**
```python
# Core Domain (tu lógica)
class GoChessEngine:  # Puerto
    def place_piece() -> GameResult
    def move_piece() -> GameResult

# Adapters
class FastAPIAdapter:     # Adaptador Web
class WebSocketAdapter:   # Adaptador WebSocket
class InMemoryAdapter:    # Adaptador Storage
```

#### **2. Command Pattern (Movimientos)**
```python
@dataclass
class GameCommand:
    type: str  # "place_piece", "move_piece", "switch_phase"
    payload: dict
    player_id: str
    timestamp: datetime

class CommandHandler:
    def execute(command: GameCommand) -> GameResult
```

#### **3. Observer Pattern (State Updates)**
```python
class GameStateObserver:
    def on_game_updated(game_id: str, new_state: GameState)
    def on_player_connected(game_id: str, player_id: str)
    def on_error(game_id: str, error: GameError)
```

#### **4. Repository Pattern (Future-Proof Storage)**
```python
class GameRepository(ABC):
    def save_game(game: GameState) -> None
    def load_game(game_id: str) -> GameState
    
# Implementaciones
class InMemoryRepository(GameRepository)  # Fase actual
class PostgreSQLRepository(GameRepository)  # Fase futura
```

## Fases de Desarrollo Detalladas

### **FASE 1: Core Logic Foundation (Semana 1-2)**

#### **Decisiones Arquitectónicas**
- **Patrón:** Domain-Driven Design para el motor del juego
- **Testing:** TDD con pytest para validaciones críticas
- **Structure:** Separación clara entre reglas de ajedrez y reglas Go-Chess
- **Simplicidad:** Evitar complejidades iniciales, enfocarse en la lógica del juego

#### **Implementación**
```python
# Estructura de directorios
src/
├── domain/
│   ├── entities/           # Piece, Board, GameState
│   ├── value_objects/      # Position, Color, PieceType
│   ├── services/          # GoChessEngine, RuleValidator
│   └── exceptions/        # InvalidMoveError, GameError
├── infrastructure/        # (vacío por ahora)
└── tests/
    ├── unit/              # Tests de lógica pura
    └── integration/       # Tests de flujo completo
```

#### **Entregables**
- [ ] Clases base: `Piece`, `Board`, `Position`
- [ ] `GoChessEngine` con ambas fases
- [ ] Validador de colocación 
    - jaque
    - distancia coronación
- [ ] Validador de movimientos estándar de ajedrez
    - jaque, mate , tablas
- [ ] Suite de tests unitarios (>90% cobertura)
- [ ] Juego funcional por consola

#### **Patrones Específicos**
- **Factory Pattern** para crear piezas
- **Strategy Pattern** para diferentes validadores
- **State Pattern** para fases del juego



### **FASE 2: Configuration & Web Foundation (Semana 3)**

#### **Decisiones Arquitectónicas**
- **Frontend:** React con Context API para estado global
- **Styling:** Tailwind CSS para prototipado rápido
- **Build:** Vite para desarrollo rápido

#### **Backend Configuration System**
```python
@dataclass
class GameConfiguration:
    allowed_pieces: Dict[PieceType, int]
    max_placement_turns: Optional[int] = None
    pawn_promotion_distance: int = 2
    enable_castling: bool = True
    
class ConfigurationService:
    def load_preset(name: str) -> GameConfiguration
    def validate_configuration(config: GameConfiguration) -> List[str]

# Presets predefinidos
PRESETS = {
    "standard": GameConfiguration(...),
    "minimal": GameConfiguration(allowed_pieces={"king": 1, "pawn": 4}),
    "no_pawns": GameConfiguration(...)
}
```

#### **Frontend Architecture**
```javascript
src/
├── components/
│   ├── game/              # GameBoard, PieceSelector, GameStatus  
│   ├── config/            # ConfigPanel, PresetSelector
│   └── common/            # Button, Modal, Loading
├── hooks/                 # useGameState, useWebSocket
├── contexts/              # GameContext, ConfigContext  
├── services/              # api.js, websocket.js
└── utils/                 # constants.js, helpers.js
```

#### **Entregables**
- [ ] Sistema de configuración completo
- [ ] Interfaz web básica (tablero + configuración)
- [ ] Juego local funcional (2 jugadores, 1 PC)
- [ ] FastAPI con endpoints básicos
- [ ] Validación de configuraciones

#### **Patrones Específicos**
- **Builder Pattern** para configuraciones complejas
- **Context API** para estado global React
- **Custom Hooks** para lógica reutilizable

### **FASE 3: Multijugador Básico (Semana 4-5)**

#### **Decisiones Arquitectónicas**
- **Comunicación:** WebSocket para tiempo real + HTTP para setup
- **State Management:** In-memory con estructura para futura persistencia
- **Connection Handling:** Reconexión automática con backoff exponencial

#### **Sistema de Salas**
```python
@dataclass
class GameRoom:
    id: str                    # Código de 6 dígitos
    config: GameConfiguration
    players: Dict[str, Player] # player_id -> Player
    game_engine: GoChessEngine
    created_at: datetime
    last_activity: datetime

class RoomManager:
    rooms: Dict[str, GameRoom] = {}
    
    def create_room(config: GameConfiguration) -> str
    def join_room(room_id: str, player_id: str) -> bool
    def get_room(room_id: str) -> Optional[GameRoom]
    def cleanup_inactive_rooms() -> None
```

#### **WebSocket Manager**
```python
class WebSocketManager:
    connections: Dict[str, Dict[str, WebSocket]] = {}  # room_id -> {player_id -> ws}
    
    async def connect(room_id: str, player_id: str, websocket: WebSocket)
    async def disconnect(room_id: str, player_id: str)
    async def broadcast_to_room(room_id: str, message: dict)
    async def send_to_player(room_id: str, player_id: str, message: dict)
```

#### **Message Protocol**
```typescript
// Client -> Server
type ClientMessage = 
    | { type: "place_piece", piece: string, position: Position }
    | { type: "move_piece", from: Position, to: Position }
    | { type: "switch_phase" }
    | { type: "ping" }

// Server -> Client  
type ServerMessage =
    | { type: "game_state", data: GameState }
    | { type: "player_joined", player_id: string }
    | { type: "error", message: string }
    | { type: "pong" }
```

#### **Frontend Connection Management**
```javascript
// Custom Hook para WebSocket
const useGameConnection = (roomId) => {
    const [socket, setSocket] = useState(null);
    const [connectionStatus, setConnectionStatus] = useState('disconnected');
    const [gameState, setGameState] = useState(null);

    const connect = useCallback(() => {
        const ws = new WebSocket(`ws://localhost:8000/ws/${roomId}`);
        
        ws.onopen = () => setConnectionStatus('connected');
        ws.onclose = () => setConnectionStatus('disconnected');
        ws.onmessage = handleMessage;
        
        setSocket(ws);
    }, [roomId]);

    return { socket, connectionStatus, gameState, connect };
};
```

#### **Entregables**
- [ ] Sistema de códigos de sala (6 dígitos)
- [ ] WebSocket server con manejo de conexiones
- [ ] Sincronización de estado en tiempo real
- [ ] Interfaz para crear/unirse a salas
- [ ] Manejo básico de desconexiones
- [ ] Sistema de reconexión automática

#### **Patrones Específicos**
- **Mediator Pattern** para WebSocket manager
- **Observer Pattern** para updates de estado
- **Singleton Pattern** para room manager

## Setup de Desarrollo

### **Estructura de Proyecto**
```
go-chess/
├── backend/
│   ├── src/
│   │   ├── domain/        # Lógica del juego
│   │   ├── infrastructure/ # FastAPI, WebSocket
│   │   └── application/   # Casos de uso, servicios
│   ├── tests/
│   ├── requirements.txt
│   └── main.py
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── docs/
└── README.md
```

### **Scripts de Desarrollo**
```bash
# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend setup
cd frontend  
npm install
npm run dev

# Testing
cd backend && python -m pytest
cd frontend && npm test
```

### **Herramientas Recomendadas**
- **Backend:** FastAPI, Uvicorn, Pytest, Black (formatter)
- **Frontend:** React, Vite, Tailwind CSS, Vitest (testing)
- **Development:** Docker Compose (opcional), ngrok (para testing remoto)

## Consideraciones Adicionales

### **Testing Strategy**
- **Unit Tests:** Lógica del juego (domain layer)
- **Integration Tests:** API endpoints + WebSocket
- **E2E Tests:** Flujo completo de una partida

### **Error Handling**
- Validación exhaustiva de movimientos
- Timeouts para conexiones inactivas
- Graceful degradation si falla WebSocket

### **Performance Considerations**
- Throttling de mensajes WebSocket
- Cleanup automático de salas vacías
- Optimización de re-renders en React

### **Future-Proofing**
- Repository pattern para fácil adición de persistencia
- Configuration system extensible
- API versionada para cambios futuros

¿Te parece completo el plan? ¿Hay alguna fase o aspecto específico que quieras que desarrolle más en detalle?