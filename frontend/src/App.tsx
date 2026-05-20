import { Footer } from "./components/Footer";
import { useGame } from "./hooks/useGame";
import { STATUS } from "./state/gameReducer";
import { GameScreen } from "./screens/GameScreen";
import { MenuScreen } from "./screens/MenuScreen";
import styles from "./App.module.css";

/** Componente raíz: alterna entre el menú y la pantalla de partida. */
export function App() {
  const game = useGame();
  const isMenu = game.state.status === STATUS.MENU;

  return (
    <main className={styles.app}>
      <div className={styles.shell}>
        {isMenu ? (
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
      {/* El crédito vive en el menú; en la partida se muestra al pie. */}
      {!isMenu && <Footer />}
    </main>
  );
}
