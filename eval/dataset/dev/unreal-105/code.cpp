#include "CoreMinimal.h"

struct FCombatMath {
    static float CalculateEffectiveDamage(float RawDamage, float Armor, float MinDamage) {
        float Reduction = FMath::Clamp(Armor * 0.05f, 0.0f, 0.8f);
        float FinalDamage = RawDamage * (1.0f - Reduction);
        return FMath::Max(FinalDamage, MinDamage);
    }
};
