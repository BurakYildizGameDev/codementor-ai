// CodeMentor AI — Unreal Engine stub başlığı (mimari §5.2.2, ADR-0007/0009).
//
// Tier 1'de Unreal C++ kodu `clang++ -fsyntax-only -include ue_stubs.h -` ile denetlenir.
// Gerçek Unreal başlıkları olmadığı için burada yalnızca en sık kullanılan makrolar ve
// tiplerin minimal bildirimleri vardır. Buradaki eksiklikten doğan hatalar (tanımsız
// tanımlayıcı vb.) raporda WARNING'e düşürülür; kesin hata sayılmaz.
//
// Bu dosya derleyiciye bizim tarafımızdan verilir; kullanıcı kodu değildir.
#pragma once

#include <cstddef>
#include <cstdint>
#include <initializer_list>
#include <utility>

// ---------------------------------------------------------------- Yansıtma makroları
#define UCLASS(...)
#define USTRUCT(...)
#define UENUM(...)
#define UINTERFACE(...)
#define UPROPERTY(...)
#define UFUNCTION(...)
#define UPARAM(...)
#define UMETA(...)
#define GENERATED_BODY(...)
#define GENERATED_UCLASS_BODY(...)
#define GENERATED_USTRUCT_BODY(...)
#define GENERATED_IINTERFACE_BODY(...)

// ---------------------------------------------------------------- Yardımcı makrolar
#define TEXT(x) L##x
#define UE_LOG(Category, Verbosity, Format, ...) ((void)0)
#define check(expr) ((void)(expr))
#define checkf(expr, ...) ((void)(expr))
#define ensure(expr) (!!(expr))
#define ensureMsgf(expr, ...) (!!(expr))
#define verify(expr) ((void)(expr))
#define FORCEINLINE inline

// ---------------------------------------------------------------- Delegeler (Faz H3)
// Dinamik çok noktaya yayın delegeleri: alan olarak kullanılabilen boş bir struct üretir.
// Makro parametreleri (parametre tipleri/adları) gövdede kullanılmaz; yalnızca derleyiciye
// tip denetimi yaptırmak için alınır.
struct FStubMulticastDelegate {
    template <typename... Args>
    void Broadcast(Args&&...) const {}
    template <typename ObjectType, typename MethodType>
    void AddDynamic(ObjectType* Object, MethodType Method) {
        (void)Object; (void)Method;
    }
    template <typename ObjectType, typename MethodType>
    void RemoveDynamic(ObjectType* Object, MethodType Method) {
        (void)Object; (void)Method;
    }
    template <typename ObjectType, typename MethodType>
    void RemoveAll(ObjectType* Object) { (void)Object; }
    void Clear() {}
    bool IsBound() const { return false; }
};

#define DECLARE_DYNAMIC_MULTICAST_DELEGATE(Name, ...) \
    struct Name : public FStubMulticastDelegate {}
#define DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(Name, ...) \
    struct Name : public FStubMulticastDelegate {}
#define DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(Name, ...) \
    struct Name : public FStubMulticastDelegate {}
#define DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(Name, ...) \
    struct Name : public FStubMulticastDelegate {}
#define DECLARE_DYNAMIC_MULTICAST_DELEGATE_FourParams(Name, ...) \
    struct Name : public FStubMulticastDelegate {}
#define DECLARE_DYNAMIC_MULTICAST_DELEGATE_FiveParams(Name, ...) \
    struct Name : public FStubMulticastDelegate {}

// ---------------------------------------------------------------- Temel tipler
using int8 = std::int8_t;
using int16 = std::int16_t;
using int32 = std::int32_t;
using int64 = std::int64_t;
using uint8 = std::uint8_t;
using uint16 = std::uint16_t;
using uint32 = std::uint32_t;
using uint64 = std::uint64_t;
using TCHAR = wchar_t;

class FString {
public:
    FString() = default;
    FString(const TCHAR* Text) { (void)Text; }
    int32 Len() const { return 0; }
    bool IsEmpty() const { return true; }
    const TCHAR* operator*() const { return L""; }
    FString operator+(const FString& Other) const { (void)Other; return *this; }
    FString& operator+=(const FString& Other) { (void)Other; return *this; }
    bool operator==(const FString& Other) const { (void)Other; return true; }
    bool operator!=(const FString& Other) const { (void)Other; return false; }
    template <typename... Args>
    static FString Printf(const TCHAR* Format, Args&&...) { (void)Format; return FString(); }
    static FString FromInt(int32 Value) { (void)Value; return FString(); }
};

class FName {
public:
    FName() = default;
    FName(const TCHAR* Text) { (void)Text; }
    FString ToString() const { return FString(); }
    bool IsNone() const { return true; }
    bool operator==(const FName& Other) const { (void)Other; return true; }
    bool operator!=(const FName& Other) const { (void)Other; return false; }
    bool operator<(const FName& Other) const { (void)Other; return false; }
};

class FText {
public:
    static FText FromString(const FString& Text) { (void)Text; return FText(); }
    FString ToString() const { return FString(); }
};

struct FVector {
    double X = 0, Y = 0, Z = 0;
    FVector() = default;
    FVector(double InX, double InY, double InZ) : X(InX), Y(InY), Z(InZ) {}
    FVector operator+(const FVector& V) const { return FVector(X + V.X, Y + V.Y, Z + V.Z); }
    FVector operator-(const FVector& V) const { return FVector(X - V.X, Y - V.Y, Z - V.Z); }
    FVector operator*(double Scale) const { return FVector(X * Scale, Y * Scale, Z * Scale); }
    FVector& operator+=(const FVector& V) { X += V.X; Y += V.Y; Z += V.Z; return *this; }
    double Size() const { return 0; }
    double SizeSquared() const { return 0; }
    FVector GetSafeNormal() const { return *this; }
    static double Dist(const FVector& A, const FVector& B) { (void)A; (void)B; return 0; }
    static double DistSquared(const FVector& A, const FVector& B) { (void)A; (void)B; return 0; }
    static const FVector ZeroVector;
};
inline const FVector FVector::ZeroVector{};

struct FRotator {
    double Pitch = 0, Yaw = 0, Roll = 0;
    FRotator() = default;
    FRotator(double InPitch, double InYaw, double InRoll) : Pitch(InPitch), Yaw(InYaw), Roll(InRoll) {}
    static const FRotator ZeroRotator;
};
inline const FRotator FRotator::ZeroRotator{};

struct FTransform {
    FVector GetLocation() const { return FVector(); }
    FRotator Rotator() const { return FRotator(); }
};

// ---------------------------------------------------------------- Matematik ve çarpışma
struct FMath {
    template <typename T>
    static T Clamp(T Value, T MinValue, T MaxValue) {
        if (Value < MinValue) return MinValue;
        if (Value > MaxValue) return MaxValue;
        return Value;
    }
    template <typename T>
    static T Abs(T Value) {
        if constexpr (T(-1) < T(0)) {  // işaretsiz tipte karşılaştırma uyarısı doğmasın
            return Value < T(0) ? -Value : Value;
        }
        return Value;
    }
    template <typename T>
    static T Max(T A, T B) { return A > B ? A : B; }
    template <typename T>
    static T Min(T A, T B) { return A < B ? A : B; }
    template <typename T>
    static T Sqrt(T Value) { (void)Value; return T(); }
};

struct FHitResult {
    bool bBlockingHit = false;
    bool bStartPenetrating = false;
    float Time = 0.0f;
    float Distance = 0.0f;
    int32 Item = -1;
    FVector Location;
    FVector ImpactPoint;
    FVector Normal;
    FVector ImpactNormal;
    FName BoneName;
    FName MyBoneName;
    class AActor* GetActor() const { return nullptr; }
    class UPrimitiveComponent* GetComponent() const { return nullptr; }
};

struct FTimerHandle {
    bool IsValid() const { return false; }
    void Invalidate() {}
};

class FTimerManager {
public:
    // Unreal'da `SetTimer` çok biçimlidir (TFunction, üye fonksiyon işaretçisi, lambda):
    // stub her çağrıyı kabul eder, tip denetimi kullanıcı kodunda kalır.
    template <typename... Args>
    void SetTimer(FTimerHandle& InOutHandle, Args&&... InArgs) {
        (void)InOutHandle;
        ((void)InArgs, ...);
    }
    template <typename... Args>
    void SetTimerForNextTick(Args&&... InArgs) {
        ((void)InArgs, ...);
    }
    void ClearTimer(FTimerHandle& InOutHandle) { (void)InOutHandle; }
    void ClearAllTimersForObject(const class UObject* Object) { (void)Object; }
    bool IsTimerActive(const FTimerHandle& InHandle) const { (void)InHandle; return false; }
    float GetTimerRemaining(const FTimerHandle& InHandle) const {
        (void)InHandle;
        return 0.0f;
    }
};

// ---------------------------------------------------------------- Kapsayıcılar
template <typename T>
class TArray {
public:
    TArray() = default;
    TArray(std::initializer_list<T> Items) { (void)Items; }
    int32 Add(const T& Item) { (void)Item; return 0; }
    template <typename... Args>
    int32 Emplace(Args&&...) { return 0; }
    int32 AddUnique(const T& Item) { (void)Item; return 0; }
    int32 Num() const { return 0; }
    bool IsEmpty() const { return true; }
    bool IsValidIndex(int32 Index) const { (void)Index; return false; }
    bool Contains(const T& Item) const { (void)Item; return false; }
    int32 Find(const T& Item) const { (void)Item; return -1; }
    int32 Remove(const T& Item) { (void)Item; return 0; }
    int32 RemoveSwap(const T& Item) { (void)Item; return 0; }
    void RemoveAt(int32 Index) { (void)Index; }
    void RemoveAtSwap(int32 Index) { (void)Index; }
    void Empty(int32 Slack = 0) { (void)Slack; }
    void Reset(int32 Slack = 0) { (void)Slack; }
    void Reserve(int32 Number) { (void)Number; }
    void SetNum(int32 Number) { (void)Number; }
    void Sort() {}
    T& Last() { return *Data; }
    T Pop() { return *Data; }
    T& operator[](int32 Index) { (void)Index; return *Data; }
    const T& operator[](int32 Index) const { (void)Index; return *Data; }
    T* begin() { return Data; }
    T* end() { return Data; }
    const T* begin() const { return Data; }
    const T* end() const { return Data; }
private:
    T* Data = nullptr;
};

template <typename K, typename V>
struct TPair {
    K Key;
    V Value;
};

template <typename K, typename V>
class TMap {
public:
    V& Add(const K& Key, const V& Value) { (void)Key; (void)Value; return *Found; }
    V& Add(const K& Key) { (void)Key; return *Found; }
    V* Find(const K& Key) { (void)Key; return Found; }
    const V* Find(const K& Key) const { (void)Key; return Found; }
    V& FindOrAdd(const K& Key) { (void)Key; return *Found; }
    bool Contains(const K& Key) const { (void)Key; return false; }
    int32 Remove(const K& Key) { (void)Key; return 0; }
    int32 Num() const { return 0; }
    void Empty() {}
    V& operator[](const K& Key) { (void)Key; return *Found; }
    TPair<K, V>* begin() { return Pairs; }
    TPair<K, V>* end() { return Pairs; }
    const TPair<K, V>* begin() const { return Pairs; }
    const TPair<K, V>* end() const { return Pairs; }
private:
    V* Found = nullptr;
    TPair<K, V>* Pairs = nullptr;
};

template <typename T>
class TSet {
public:
    void Add(const T& Item) { (void)Item; }
    bool Contains(const T& Item) const { (void)Item; return false; }
    int32 Remove(const T& Item) { (void)Item; return 0; }
    int32 Num() const { return 0; }
    void Empty() {}
    T* begin() { return Data; }
    T* end() { return Data; }
    const T* begin() const { return Data; }
    const T* end() const { return Data; }
private:
    T* Data = nullptr;
};

// ---------------------------------------------------------------- Nesne modeli
class UWorld;
class UClass;

class UObject {
public:
    UClass* GetClass() const { return nullptr; }
    virtual ~UObject() = default;
    UWorld* GetWorld() const { return nullptr; }
    FName GetFName() const { return FName(); }
    FString GetName() const { return FString(); }
    bool IsValidLowLevel() const { return true; }
};

class UClass : public UObject {};

class UActorComponent;

enum ELevelTick { LEVELTICK_TimeOnly, LEVELTICK_ViewportsOnly, LEVELTICK_All, LEVELTICK_PauseTick };
struct FActorComponentTickFunction {};

class AActor : public UObject {
public:
    virtual void BeginPlay() {}
    virtual void EndPlay() {}
    virtual void Tick(float DeltaSeconds) { (void)DeltaSeconds; }
    FVector GetActorLocation() const { return FVector(); }
    bool SetActorLocation(const FVector& NewLocation) { (void)NewLocation; return true; }
    FRotator GetActorRotation() const { return FRotator(); }
    FTransform GetActorTransform() const { return FTransform(); }
    bool Destroy() { return true; }
    template <typename T>
    T* FindComponentByClass() const { return nullptr; }
    FTimerManager& GetWorldTimerManager() const {
        static FTimerManager Manager;  // stub: gerçek dünya zamanlayıcısı yerine sabit örnek
        return Manager;
    }
    struct FActorTickFunction { bool bCanEverTick = false; bool bStartWithTickEnabled = true; };
    FActorTickFunction PrimaryActorTick;
};

class UActorComponent : public UObject {
public:
    virtual void BeginPlay() {}
    virtual void TickComponent(float DeltaTime, ELevelTick TickType,
                               FActorComponentTickFunction* ThisTickFunction) {
        (void)DeltaTime; (void)TickType; (void)ThisTickFunction;
    }
    AActor* GetOwner() const { return nullptr; }
    FTimerManager& GetWorldTimerManager() const {
        static FTimerManager Manager;
        return Manager;
    }
};

class UWorld : public UObject {
public:
    float GetTimeSeconds() const { return 0.0f; }
    float GetDeltaSeconds() const { return 0.0f; }
    template <typename T>
    T* SpawnActor(UClass* Class, const FVector& Location, const FRotator& Rotation) {
        (void)Class; (void)Location; (void)Rotation; return nullptr;
    }
};

// ---------------------------------------------------------------- İşaretçi sarmalayıcıları
template <typename T>
class TObjectPtr {
public:
    TObjectPtr() = default;
    TObjectPtr(T* InPtr) : Ptr(InPtr) {}
    T* Get() const { return Ptr; }
    T* operator->() const { return Ptr; }
    T& operator*() const { return *Ptr; }
    operator T*() const { return Ptr; }
    explicit operator bool() const { return Ptr != nullptr; }
private:
    T* Ptr = nullptr;
};

template <typename T>
class TWeakObjectPtr {
public:
    TWeakObjectPtr() = default;
    TWeakObjectPtr(T* InPtr) : Ptr(InPtr) {}
    T* Get() const { return Ptr; }
    bool IsValid() const { return Ptr != nullptr; }
    void Reset() { Ptr = nullptr; }
    T* operator->() const { return Ptr; }
    explicit operator bool() const { return Ptr != nullptr; }
private:
    T* Ptr = nullptr;
};

template <typename T>
class TSharedPtr {
public:
    TSharedPtr() = default;
    T* Get() const { return Ptr; }
    bool IsValid() const { return Ptr != nullptr; }
    void Reset() { Ptr = nullptr; }
    T* operator->() const { return Ptr; }
    T& operator*() const { return *Ptr; }
    explicit operator bool() const { return Ptr != nullptr; }
private:
    T* Ptr = nullptr;
};

template <typename T, typename... Args>
TSharedPtr<T> MakeShared(Args&&...) { return TSharedPtr<T>(); }

template <typename T>
class TSubclassOf {
public:
    TSubclassOf() = default;
    TSubclassOf(UClass* InClass) : Class(InClass) {}
    UClass* Get() const { return Class; }
    operator UClass*() const { return Class; }
    explicit operator bool() const { return Class != nullptr; }
private:
    UClass* Class = nullptr;
};

template <typename To, typename From>
To* Cast(From* Source) { (void)Source; return nullptr; }

inline bool IsValid(const UObject* Object) { return Object != nullptr; }
