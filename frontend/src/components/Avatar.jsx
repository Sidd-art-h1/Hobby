const PALETTE = ["#5C7A45", "#C4703A", "#374A27", "#A2582B", "#496134"];

function hashColor(str = "") {
  let h = 0;
  for (let i = 0; i < str.length; i++) h = str.charCodeAt(i) + ((h << 5) - h);
  return PALETTE[Math.abs(h) % PALETTE.length];
}

export default function Avatar({ firstname = "", lastname = "", size = 36 }) {
  const initials = `${firstname?.[0] ?? ""}${lastname?.[0] ?? ""}`.toUpperCase() || "?";
  const bg = hashColor(firstname + lastname);
  return (
    <div
      className="rounded-full flex items-center justify-center font-semibold text-white shrink-0"
      style={{ width: size, height: size, backgroundColor: bg, fontSize: size * 0.4 }}
    >
      {initials}
    </div>
  );
}
