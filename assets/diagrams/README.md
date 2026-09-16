# Diagram exports

PNG renders of every Mermaid diagram in the repository, one per diagram.
The Mermaid source inline in each markdown file is the original, and GitHub
renders it in place. These exports exist for reading offline, or in a viewer
that does not render Mermaid.

Each file is named after the document it came from.

| Export | Source |
|---|---|
| `03-architecture__3_0-solution-strategy.png` | [03-architecture/3_0-solution-strategy.md](../../03-architecture/3_0-solution-strategy.md) |
| `03-architecture__3_1-system-context.png` | [03-architecture/3_1-system-context.md](../../03-architecture/3_1-system-context.md) |
| `03-architecture__3_10-diagram-legend.png` | [03-architecture/3_10-diagram-legend.md](../../03-architecture/3_10-diagram-legend.md) |
| `03-architecture__3_2-container-view.png` | [03-architecture/3_2-container-view.md](../../03-architecture/3_2-container-view.md) |
| `03-architecture__3_3-domain-model.png` | [03-architecture/3_3-domain-model.md](../../03-architecture/3_3-domain-model.md) |
| `03-architecture__3_5-connectivity-and-edge.png` | [03-architecture/3_5-connectivity-and-edge.md](../../03-architecture/3_5-connectivity-and-edge.md), the layers |
| `03-architecture__3_5-connectivity-and-edge-1.png` | [03-architecture/3_5-connectivity-and-edge.md](../../03-architecture/3_5-connectivity-and-edge.md), the partition and reconciliation sequence |
| `04-ai-scenarios__accessibility-and-translation.png` | [04-ai-scenarios/accessibility-and-translation/README.md](../../04-ai-scenarios/accessibility-and-translation/README.md) |
| `04-ai-scenarios__animal-welfare-aquatic.png` | [04-ai-scenarios/animal-welfare-aquatic/README.md](../../04-ai-scenarios/animal-welfare-aquatic/README.md) |
| `04-ai-scenarios__animal-welfare-terrestrial.png` | [04-ai-scenarios/animal-welfare-terrestrial/README.md](../../04-ai-scenarios/animal-welfare-terrestrial/README.md) |
| `04-ai-scenarios__footfall-and-staffing.png` | [04-ai-scenarios/footfall-and-staffing/README.md](../../04-ai-scenarios/footfall-and-staffing/README.md) |
| `04-ai-scenarios__piranha-population.png` | [04-ai-scenarios/piranha-population/README.md](../../04-ai-scenarios/piranha-population/README.md) |
| `04-ai-scenarios__predictive-maintenance.png` | [04-ai-scenarios/predictive-maintenance/README.md](../../04-ai-scenarios/predictive-maintenance/README.md) |
| `04-ai-scenarios__ticketing-and-passes.png` | [04-ai-scenarios/ticketing-and-passes/README.md](../../04-ai-scenarios/ticketing-and-passes/README.md) |
| `04-ai-scenarios__visitor-experience.png` | [04-ai-scenarios/visitor-experience/README.md](../../04-ai-scenarios/visitor-experience/README.md) |
| `05-ai-assurance__5_6-cold-start-strategy.png` | [05-ai-assurance/5_6-cold-start-strategy.md](../../05-ai-assurance/5_6-cold-start-strategy.md) |

## Regenerating

```bash
09-ai-disclosure/checks/check-diagrams.sh . assets/diagrams
```

The checker renders every block at double scale on a white background and
overwrites what is here. If a diagram changes and this folder does not, the
markdown is right and the export is stale.
