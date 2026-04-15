# 1024 Game

A beautiful 1024 number sliding game built with Python 3. Available in both terminal and graphical versions!

## 🎮 Game Rules

- Use WASD or arrow keys to move tiles
- Combine identical numbers by moving them together
- Reach 1024 to win!
- Game ends when no more moves are possible

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher

### Installation
1. Clone or download the project
2. Navigate to the project directory
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Game

**Graphical Version (Recommended):**
```bash
python pygame_main.py
```
Features:
- Beautiful graphical interface
- Smooth tile movement animations
- Particle effects on tile merge and spawn
- Score and high score display
- Win/Game Over overlays

**Terminal Version:**
```bash
python main.py
```

## 🎯 Controls

### Graphical Version
- **↑ / W**: Move Up
- **↓ / S**: Move Down
- **← / A**: Move Left
- **→ / D**: Move Right
- **R**: Restart Game
- **ESC**: Quit Game
- **Mouse**: Click "New Game" button to restart

### Terminal Version
- **W / ↑**: Move Up
- **S / ↓**: Move Down
- **A / ←**: Move Left
- **D / →**: Move Right
- **Q**: Quit Game
- **R**: Restart Game

## 📁 Project Structure

```
1024game/
├── main.py              # Terminal version entry point
├── pygame_main.py       # Graphical version entry point
├── game.py              # Core game logic (shared)
├── ui.py                # Terminal user interface
├── utils.py             # Utility functions
├── data/
│   └── high_score.txt   # High score storage
├── requirements.txt     # Python dependencies
├── requirements.md      # Detailed requirements
└── README.md           # This file
```

## 🔧 Features

### Core Features
- ✅ 4x4 game grid
- ✅ Number merging mechanics
- ✅ Score tracking
- ✅ High score persistence
- ✅ Cross-platform compatibility

### Graphical Version Features
- 🎨 Beautiful modern UI design
- ✨ Smooth tile movement animations
- 💥 Particle effects on tile merge and spawn
- 🏆 Real-time score and high score display
- 🎮 Win and Game Over overlays
- 🖱️ Mouse and keyboard support
- 🎯 60 FPS smooth gameplay

### Terminal Version Features
- ✅ Terminal-based UI
- ✅ Simple controls
- ✅ Clean text display

## 🛠️ Development

### Code Quality
- Follows PEP 8 style guidelines
- Comprehensive error handling
- Modular design for maintainability

### Testing
Run tests with:
```bash
python -m pytest tests/
```

### Code Formatting
Format code with:
```bash
black .
```

## 📋 Requirements

See [requirements.md](requirements.md) for detailed technical specifications.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source. Feel free to use and modify.

## 🎮 Game Screenshots

```
┌─────────────────────────────────────┐
│           1024 Game                 │
├─────────────────────────────────────┤
│                                     │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐     │
│  │  2  │ │     │ │     │ │     │     │
│  └─────┘ └─────┘ └─────┘ └─────┘     │
│                                     │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐     │
│  │     │ │  4  │ │     │ │     │     │
│  └─────┘ └─────┘ └─────┘ └─────┘     │
│                                     │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐     │
│  │     │ │     │ │  8  │ │     │     │
│  └─────┘ └─────┘ └─────┘ └─────┘     │
│                                     │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐     │
│  │     │ │     │ │     │ │ 16  │     │
│  └─────┘ └─────┘ └─────┘ └─────┘     │
│                                     │
├─────────────────────────────────────┤
│ Score: 30          High Score: 156  │
├─────────────────────────────────────┤
│ Use WASD or Arrow Keys to move      │
│ Press Q to quit                     │
└─────────────────────────────────────┘
```

## 🐛 Troubleshooting

**Game won't start?**
- Ensure Python 3.8+ is installed
- Check that all files are in the same directory

**High score not saving?**
- Ensure write permissions in the data directory
- Check that `data/high_score.txt` exists

**Display issues?**
- Try resizing your terminal window
- Ensure your terminal supports UTF-8

---

Happy gaming! 🎉
