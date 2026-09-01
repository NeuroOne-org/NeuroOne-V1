"use client";

interface Node {
  id: string;
  x: number;
  y: number;
  r: number;
  color: string;
  delay: number;
}

interface Edge {
  from: string;
  to: string;
  color: string;
  delay: number;
}

// Fixed (not random) layout so server and client render identically —
// loosely arranged like cortical regions with synaptic connections
// between them. Colors cycle through the three accent tones so no
// single hue dominates.
const NODES: Node[] = [
  { id: "a", x: 60, y: 90, r: 5, color: "#35D6C8", delay: 0 },
  { id: "b", x: 180, y: 50, r: 4, color: "#6E7BFF", delay: 0.4 },
  { id: "c", x: 300, y: 110, r: 6, color: "#FF6A3D", delay: 0.9 },
  { id: "d", x: 130, y: 170, r: 4, color: "#6E7BFF", delay: 1.3 },
  { id: "e", x: 260, y: 210, r: 5, color: "#35D6C8", delay: 0.6 },
  { id: "f", x: 380, y: 180, r: 4, color: "#35D6C8", delay: 1.7 },
  { id: "g", x: 60, y: 260, r: 4, color: "#FF6A3D", delay: 2.1 },
  { id: "h", x: 220, y: 320, r: 6, color: "#6E7BFF", delay: 0.2 },
  { id: "i", x: 350, y: 300, r: 4, color: "#35D6C8", delay: 1.0 },
  { id: "j", x: 400, y: 60, r: 3, color: "#6E7BFF", delay: 1.5 },
];

const EDGES: Edge[] = [
  { from: "a", to: "b", color: "#35D6C8", delay: 0 },
  { from: "b", to: "c", color: "#6E7BFF", delay: 0.5 },
  { from: "b", to: "d", color: "#6E7BFF", delay: 1.0 },
  { from: "c", to: "e", color: "#FF6A3D", delay: 1.5 },
  { from: "d", to: "e", color: "#35D6C8", delay: 0.3 },
  { from: "d", to: "g", color: "#6E7BFF", delay: 2.0 },
  { from: "e", to: "f", color: "#35D6C8", delay: 0.8 },
  { from: "e", to: "h", color: "#FF6A3D", delay: 1.2 },
  { from: "g", to: "h", color: "#6E7BFF", delay: 0.6 },
  { from: "h", to: "i", color: "#35D6C8", delay: 1.8 },
  { from: "f", to: "i", color: "#35D6C8", delay: 0.4 },
  { from: "c", to: "j", color: "#6E7BFF", delay: 1.1 },
];

function findNode(id: string) {
  return NODES.find((n) => n.id === id)!;
}

export function NeuralNetwork({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 440 380"
      className={className}
      preserveAspectRatio="xMidYMid meet"
    >
      <defs>
        <filter id="node-glow" x="-100%" y="-100%" width="300%" height="300%">
          <feGaussianBlur stdDeviation="3" result="blur" />
          <feMerge>
            <feMergeNode in="blur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>

      {EDGES.map((edge, i) => {
        const from = findNode(edge.from);
        const to = findNode(edge.to);
        return (
          <line
            key={i}
            x1={from.x}
            y1={from.y}
            x2={to.x}
            y2={to.y}
            stroke={edge.color}
            strokeWidth={1}
            strokeOpacity={0.25}
          />
        );
      })}

      {EDGES.map((edge, i) => {
        const from = findNode(edge.from);
        const to = findNode(edge.to);
        return (
          <line
            key={`pulse-${i}`}
            x1={from.x}
            y1={from.y}
            x2={to.x}
            y2={to.y}
            stroke={edge.color}
            strokeWidth={1.5}
            pathLength={1}
            strokeDasharray="0.14 1"
            className="animate-[synapse-flow_3.2s_linear_infinite]"
            style={{
              animationDelay: `${edge.delay}s`,
              filter: "url(#node-glow)",
            }}
          />
        );
      })}

      {NODES.map((node) => (
        <circle
          key={node.id}
          cx={node.x}
          cy={node.y}
          r={node.r}
          fill={node.color}
          className="animate-node-pulse"
          style={{
            animationDelay: `${node.delay}s`,
            filter: "url(#node-glow)",
            transformOrigin: `${node.x}px ${node.y}px`,
          }}
        />
      ))}
    </svg>
  );
}
