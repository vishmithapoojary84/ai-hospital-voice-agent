export default function Avatar({ state }) {
    return (
        <div
            className={`avatar ${
                state === "speaking"
                    ? "speaking"
                    : state === "listening"
                    ? "listening"
                    : ""
            }`}
        >
            <div className="avatar-core"></div>
        </div>
    );
}
