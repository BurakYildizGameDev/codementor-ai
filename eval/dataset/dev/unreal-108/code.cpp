#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "BaseCharacter.generated.h"

UCLASS()
class ABaseCharacter : public AActor {
    GENERATED_BODY()

protected:
    virtual void BeginPlay() override;
};

void ABaseCharacter::BeginPlay() {
    int32 InitialHealth = 100;
}
