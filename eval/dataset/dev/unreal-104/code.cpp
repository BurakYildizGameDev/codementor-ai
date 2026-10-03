#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Components/StaticMeshComponent.h"
#include "SimpleActor.generated.h"

UCLASS()
class ASimpleActor : public AActor {
    GENERATED_BODY()

public:
    ASimpleActor();

protected:
    virtual void BeginPlay() override;

private:
    UPROPERTY(VisibleAnywhere)
    UStaticMeshComponent* MeshComponent;
};

void ASimpleActor::BeginPlay() {
    Super::BeginPlay();
}
