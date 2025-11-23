export const concentricOptions = {
  name: "concentric",
  fit: true,
  padding: 30,
  equidistant: false,
  avoidOverlap: false,
  startAngle: 0,
  clockwise: false,
  nodeDimensionsIncludeLabels: true,
  concentric: function (node: cytoscape.NodeSingular) {
    const nodeType = node.data("category");
    if (nodeType === "Course" || nodeType === "Concept") {
      return 1000 - (node.data("depth") as number);
    } else {
      return 1;
    }
  },
  levelWidth: function () {
    return 1;
  },
};

export function createSvgCircleProgress(percent: number, size = 40, showText = false, mastery = 0, color = "#86e059ff"): string {
  const r = size / 2;
  const c = size / 2;
  const fontSize = Math.round(size * 0.3);
  const textSvg = showText
    ? `<text x="${c}" y="${c}" text-anchor="middle" dominant-baseline="central" font-size="${fontSize}" fill="#333">${mastery}%</text>`
    : "";
  let progressSvg = "";
  if (percent >= 100) {
    // 画完整圆环
    progressSvg = `<circle cx="${c}" cy="${c}" r="${r}" stroke="${color}" stroke-width="6" fill="none"/>`;
  } else if (percent > 0) {
    const angle = (percent / 100.0) * 2 * Math.PI;
    const x = c + r * Math.cos(angle - Math.PI / 2);
    const y = c + r * Math.sin(angle - Math.PI / 2);
    const largeArc = percent > 50 ? 1 : 0;
    progressSvg = `<path d="M${c},${c - r} A${r},${r} 0 ${largeArc},1 ${x},${y}" stroke="${color}" stroke-width="6" fill="none"/>`;
  }
  const svg = `
    <svg width="${size}" height="${size}" xmlns="http://www.w3.org/2000/svg">
      <circle cx="${c}" cy="${c}" r="${r}" stroke="#eee" stroke-width="6" fill="none"/>
      ${progressSvg}
      ${textSvg}
    </svg>
  `;
  return "data:image/svg+xml;base64," + btoa(svg);
}

export const styles: cytoscape.StylesheetJson = [
  {
    selector: "node",
    style: {
      "background-color": "#00dbdd",
      label: "data(name)",
      "text-valign": "bottom",
      "text-margin-y": 3,
      "font-size": 9,
      color: "#000",
      width: "mapData(depth, 0, 4, 40, 20)",
      height: "mapData(depth, 0, 4, 40, 20)",
    },
  },
  {
    selector: 'node[depth=0]',
    style: {
      "background-color": "#f12711",
    },
  },
  {
    selector: 'node[depth=1]',
    style: {
      "background-color": "#a967ff",
    },
  },
  {
    selector: 'node[depth=2]',
    style: {
      "background-color": "#7f84df",
    },
  },
  {
    selector: 'node[depth=3]',
    style: {
      "background-color": "#55a1bf",
    },
  },
  {
    selector: 'node[depth=4]',
    style: {
      "background-color": "#2bbe9f",
    },
  },
  {
    selector: 'node[category = "Concept"]',
    style: {
      "background-image": "data(img)",
      "background-fit": "cover",
      "background-opacity": 1,
    },
  },
  {
    selector: "edge",
    style: {
      width: 1.2,
      "target-arrow-shape": "triangle",
      label: "data(relation)",
      "text-margin-y": 6,
      "font-size": 8,
      "curve-style": "bezier",
    },
  },
  {
    selector: "edge[relation = '前置']",
    style: {
      "line-color": "#409eff",
      "target-arrow-color": "#409eff",
      "line-style": "dashed",
    },
  },
  {
    selector: ":selected",
    style: {
      "background-color": "#fb9e3b",
    },
  },
  {
    selector: ".fade",
    style: {
      opacity: 0.2,
      "transition-property": "opacity",
      "transition-duration": 0.2,
    },
  },
  {
    selector: ".hover",
    style: {
    },
  },
];