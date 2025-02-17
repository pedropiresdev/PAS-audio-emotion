export function Progress({ value }) {
    return <progress value={value} max="100" className="w-full h-2 bg-gray-200" />;
}