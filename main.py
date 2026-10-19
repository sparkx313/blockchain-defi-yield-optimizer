import random
import math
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Protocol:
    name: str
    chain: str
    apy: float
    tvl_usd: float
    risk_score: float  # 0-10, lower is safer

PROTOCOLS = [
    Protocol("Aave V3", "Ethereum", 0.085, 8_500_000_000, 1.5),
    Protocol("Compound V3", "Ethereum", 0.072, 3_200_000_000, 1.8),
    Protocol("Curve 3pool", "Ethereum", 0.051, 1_800_000_000, 1.2),
    Protocol("Yearn USDC", "Ethereum", 0.112, 450_000_000, 2.5),
    Protocol("Aave V3", "Polygon", 0.094, 890_000_000, 2.0),
    Protocol("Beefy Finance", "BSC", 0.187, 320_000_000, 4.5),
    Protocol("Stargate", "Arbitrum", 0.143, 560_000_000, 3.0),
]

class YieldOptimizer:
    def __init__(self, capital: float, risk_tolerance: float = 5.0):
        self.capital = capital
        self.risk_tolerance = risk_tolerance

    def filter_safe(self, protocols: List[Protocol]) -> List[Protocol]:
        return [p for p in protocols if p.risk_score <= self.risk_tolerance]

    def optimize_allocation(self) -> Dict[str, float]:
        safe = self.filter_safe(PROTOCOLS)
        safe.sort(key=lambda p: p.apy / max(p.risk_score, 0.1), reverse=True)
        allocation = {}
        remaining = self.capital
        for i, p in enumerate(safe[:5]):
            weight = 1 / (i + 1)
            amount = remaining * weight / sum(1/(j+1) for j in range(min(5, len(safe))))
            allocation[f"{p.name} ({p.chain})"] = amount
        return allocation

    def project_returns(self, days: int = 365) -> float:
        alloc = self.optimize_allocation()
        safe = self.filter_safe(PROTOCOLS)
        safe_dict = {f"{p.name} ({p.chain})": p.apy for p in safe}
        total = 0
        for key, amount in alloc.items():
            apy = safe_dict.get(key, 0.05)
            daily = apy / 365
            total += amount * ((1 + daily)**days - 1)
        return total

if __name__ == "__main__":
    opt = YieldOptimizer(capital=100_000, risk_tolerance=5.0)
    alloc = opt.optimize_allocation()
    print("Optimal Yield Allocation:")
    for k, v in alloc.items():
        print(f"  {k:40s} ${v:,.2f}")
    returns = opt.project_returns(365)
    print(f"\nProjected Annual Returns: ${returns:,.2f} ({returns/100_000:.1%})")
