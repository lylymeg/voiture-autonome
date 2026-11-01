# 🏎️ AI Autonomous Cars — Genetic Algorithm Evolution (Pygame)

Une simulation d'intelligence artificielle combinant **Réseaux de Neurones** et **Algorithmes Génétiques**, développée en **Python** avec **Pygame**, où des voitures autonomes apprennent par essai-erreur à piloter sur un circuit.

---

## 📸 Fonctionnalités

- 🧬 **Algorithme Génétique (Évolution) :** Chaque génération de voitures teste un parcours. Les meilleures survivent, transmettent et mutent leurs gènes (poids synaptiques) pour créer des pilotes de plus en plus performants.
- 👁️ **Capteurs LIDAR virtuels :** Les véhicules analysent leur environnement en temps réel pour détecter les murs et ajuster leur trajectoire.
- 🏆 **Élitisme & Apprentissage continu :** Le système met automatiquement en valeur la meilleure voiture de la génération en cours (en doré).
- 🔄 **Réinitialisation rapide :** Redémarre l'apprentissage à tout moment avec la touche `R`.

---

## 🚀 Lancement

```bash
pip install pygame
python main.py