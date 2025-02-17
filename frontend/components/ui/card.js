export function Card({ children }) {
    return <div className="p-6 bg-white shadow-lg rounded-lg"></div>
}

export function CardContent({ children, className = ""}) {
    return <div className={`p-4 ${className}`}>{children}</div>;
}