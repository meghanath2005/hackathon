# Modeling

## Baselines
- Persistence forecast extrapolates latest 6-hour displacement.
- GRU regressor predicts next `(lat, lon)` from a short sequence window.

## Hybrid model
- GRU encoder compresses sequence context.
- 4-qubit PennyLane variational circuit transforms compressed features.
- Dense head projects quantum expectations to coordinate outputs.

This is a simulator-based hybrid experiment; no claim of proven quantum advantage.
