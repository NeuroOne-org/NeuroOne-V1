interface Particle {
  x: number; // percent
  y: number; // percent
  size: number;
  color: string;
  delay: number;
  duration: number;
}

// Fixed positions (not randomized) so the layout is stable across
// server/client renders. Varying size + duration gives a loose
// parallax feel — smaller, slower dots read as "further back."
const PARTICLES: Particle[] = [
  { x: 12, y: 15, size: 3, color: "#35D6C8", delay: 0, duration: 7 },
  { x: 82, y: 10, size: 2, color: "#6E7BFF", delay: 1.2, duration: 6 },
  { x: 65, y: 28, size: 4, color: "#FF6A3D", delay: 0.6, duration: 8 },
  { x: 30, y: 40, size: 2, color: "#6E7BFF", delay: 2.1, duration: 5.5 },
  { x: 90, y: 45, size: 3, color: "#35D6C8", delay: 1.8, duration: 7.5 },
  { x: 8, y: 60, size: 2, color: "#FF6A3D", delay: 0.3, duration: 6.5 },
  { x: 50, y: 70, size: 3, color: "#6E7BFF", delay: 2.6, duration: 8.2 },
  { x: 75, y: 80, size: 2, color: "#35D6C8", delay: 1.0, duration: 6 },
  { x: 20, y: 85, size: 4, color: "#6E7BFF", delay: 0.8, duration: 7.2 },
  { x: 95, y: 65, size: 2, color: "#FF6A3D", delay: 1.6, duration: 5.8 },
];

export function FloatingParticles({ className }: { className?: string }) {
  return (
    <div
      className={className}
      style={{ perspective: "600px", transformStyle: "preserve-3d" }}
    >
      {PARTICLES.map((p, i) => (
        <div
          key={i}
          className="absolute animate-float-particle rounded-full"
          style={{
            left: `${p.x}%`,
            top: `${p.y}%`,
            width: p.size,
            height: p.size,
            backgroundColor: p.color,
            boxShadow: `0 0 ${p.size * 3}px ${p.color}`,
            animationDelay: `${p.delay}s`,
            animationDuration: `${p.duration}s`,
          }}
        />
      ))}
    </div>
  );
}
