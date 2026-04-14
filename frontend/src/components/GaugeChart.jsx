import {
  RadialBarChart,
  RadialBar,
  PolarAngleAxis,
  ResponsiveContainer
} from "recharts";

function getScoreColor(score) {
  if (score <= 25) return "#16a34a";
  if (score <= 50) return "#eab308";
  if (score <= 75) return "#f97316";
  return "#dc2626";
}

function getScoreLabel(score) {
  if (score <= 25) return "Riesgo bajo";
  if (score <= 50) return "Riesgo moderado";
  if (score <= 75) return "Riesgo alto";
  return "Riesgo muy alto";
}

export default function GaugeChart({ score }) {
  const gaugeColor = getScoreColor(score);
  const riskLabel = getScoreLabel(score);

  const data = [
    {
      name: "score",
      value: score,
      fill: gaugeColor
    }
  ];

  return (
    <div className="card glass-card">
      <div className="card-top">
        <h2 className="card-title">Manipulación lingüística</h2>
        <span className="status-chip" style={{ backgroundColor: gaugeColor }}>
          {riskLabel}
        </span>
      </div>

      <div className="gauge-wrapper">
        <div className="gauge-chart-box">
          <ResponsiveContainer width="100%" height={260}>
            <RadialBarChart
              cx="50%"
              cy="85%"
              innerRadius="65%"
              outerRadius="100%"
              barSize={24}
              data={data}
              startAngle={180}
              endAngle={0}
            >
              <PolarAngleAxis
                type="number"
                domain={[0, 100]}
                tick={false}
              />
              <RadialBar
                dataKey="value"
                background={{ fill: "var(--gauge-track)" }}
                clockWise
                cornerRadius={18}
              />
            </RadialBarChart>
          </ResponsiveContainer>
        </div>

        <div className="gauge-score" style={{ color: gaugeColor }}>
          {score}%
        </div>

        <div className="gauge-label">Semáforo de probabilidad de desinformación</div>

        <div className="gauge-scale">
          <span className="scale-dot green"></span>
          <span className="scale-dot yellow"></span>
          <span className="scale-dot orange"></span>
          <span className="scale-dot red"></span>
        </div>

        <div className="gauge-scale-labels">
          <span>0</span>
          <span>25</span>
          <span>50</span>
          <span>75</span>
          <span>100</span>
        </div>
      </div>
    </div>
  );
}