import { Footer } from "./components/Footer";
import { useGame } from "./hooks/useGame";
import { STATUS } from "./state/gameReducer";
import { GameScreen } from "./screens/GameScreen";
import { MenuScreen } from "./screens/MenuScreen";
import styles from "./App.module.css";

/** Componente raíz: alterna entre el menú y la pantalla de partida. */
export function App() {
  const game = useGame();

  return (
    <main className={styles.app}>
      <div className={styles.shell}>
        {game.state.status === STATUS.MENU ? (
          <MenuScreen
            config={game.state.config}
            error={game.state.error}
            onConfigChange={game.updateConfig}
            onStart={game.startGame}
          />
        ) : (
          <GameScreen game={game} />
        )}
      </div>
      <Footer />
    </main>
  );
}
