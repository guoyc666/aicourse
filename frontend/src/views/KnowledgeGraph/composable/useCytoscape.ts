import type { CytoscapeElements, KnowledgeEdge, KnowledgeNode } from "../../../types";

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

export function convertGraphToElements(
  nodes: KnowledgeNode[],
  edges: KnowledgeEdge[],
  progressRecords: Record<string, number>,
  masteryRecords: Record<string, number>
): CytoscapeElements {
  const cytoNodes = nodes.map((node) => {
    if (node.category === "Course") {
      return {
        data: {
          id: node.id,
          name: node.name,
          category: node.category,
          description: node.description,
          depth: 0,
          expanded: true,
          img: "",
        },
      };
    } else {
      return {
        data: {
          id: node.id,
          name: node.name,
          category: node.category,
          description: node.description,
          depth: node.depth,
          expanded: false,
          img: createSvgCircleProgress(
            progressRecords[node.id] || 0,
            masteryRecords[node.id] || 0,
            Math.max(44 - node.depth * 8, 20)
          ),
        },
      };
    }
  });

  const cytoEdges = edges
  .map(edge => ({
    data: {
      source: edge.source,
      target: edge.target,
      relation: edge.relation,
    },
  }));
  return { nodes: cytoNodes, edges: cytoEdges };
};

export function convertElementsToGraph( elements: CytoscapeElements ) {
  const nodes: KnowledgeNode[] = elements.nodes.map((cyNode) => {
    if (cyNode.data.category === "Course") {
      return {
        id: cyNode.data.id,
        name: cyNode.data.name,
        description: cyNode.data.description,
        category: "Course",
        depth: cyNode.data.depth,
      };
    } else {
      return {
        id: cyNode.data.id,
        name: cyNode.data.name,
        description: cyNode.data.description,
        category: "Concept",
        depth: cyNode.data.depth,
      };
    }
  });

  const edges: KnowledgeEdge[] = elements.edges.map((cyEdge) => ({
    source: cyEdge.data.source,
    target: cyEdge.data.target,
    relation: cyEdge.data.relation,
  }));
  return { nodes, edges };
}

export function createSvgCircleProgress(progress = 0, mastery = 0, size = 40, showText = true, color = "#86e059ff"): string {
  const progressPercent = +(progress * 100).toFixed(2);
  const masteryPercent = +(mastery * 100).toFixed(2);
  const r = size / 2;
  const c = size / 2;
  const fontSize = Math.round(size * 0.3);
  const textSvg = showText
    ? `<text x="${c}" y="${c}" text-anchor="middle" dominant-baseline="central" font-size="${fontSize}" fill="#333">${masteryPercent}%</text>`
    : "";
  let progressSvg = "";
  if (progressPercent >= 100) {
    // 画完整圆环
    progressSvg = `<circle cx="${c}" cy="${c}" r="${r}" stroke="${color}" stroke-width="6" fill="none"/>`;
  } else if (progressPercent > 0) {
    const angle = (progressPercent / 100.0) * 2 * Math.PI;
    const x = c + r * Math.cos(angle - Math.PI / 2);
    const y = c + r * Math.sin(angle - Math.PI / 2);
    const largeArc = progressPercent > 50 ? 1 : 0;
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
      width: "mapData(depth, 1, 3, 36, 20)",
      height: "mapData(depth, 1, 3, 36, 20)",
    },
  },
  {
    selector: 'node[depth=0]',
    style: {
      "background-color": "#1111f1",
      width: 60,
      height: 60,
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
    selector: '.study_status_view',
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