interface HeaderProps {
  onMenuClick: () => void;
}

function Header({
  onMenuClick,
}: HeaderProps) {
  return (
    <header className="topbar">
      <div className="topbar-left">
        <button
          type="button"
          className="mobile-menu-button"
          onClick={onMenuClick}
          aria-label="Open knowledge base"
        >
          ☰
        </button>

        <div>
          <h2>
            AI Software Engineering Assistant
          </h2>

          <p>
            Ask questions grounded in your project
            documentation.
          </p>
        </div>
      </div>

      <div className="rag-badge">
        RAG
      </div>
    </header>
  );
}

export default Header;