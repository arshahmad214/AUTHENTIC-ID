import os
import shutil
import random

# ── paths ──────────────────────────────────────────
BASE      = r"D:\ai-ml project\AuthenticID\dataset\age"
UTK_DIR   = os.path.join(BASE, "UTKFace")

OUT_TRAIN_ADULT   = os.path.join(BASE, "final", "train", "adult")
OUT_TRAIN_UNDER18 = os.path.join(BASE, "final", "train", "under_18")
OUT_TEST_ADULT    = os.path.join(BASE, "final", "test",  "adult")
OUT_TEST_UNDER18  = os.path.join(BASE, "final", "test",  "under_18")

# ── clean old output first ─────────────────────────
print("Cleaning old output...")
for folder in [OUT_TRAIN_ADULT, OUT_TRAIN_UNDER18,
               OUT_TEST_ADULT,  OUT_TEST_UNDER18]:
    if os.path.exists(folder):
        shutil.rmtree(folder,  ignore_errors=True)
    os.makedirs(folder, exist_ok=True)

# ── Sort all UTKFace images by class ──────────────
print("Reading UTKFace images...")
adult_imgs    = []
under18_imgs  = []

for img in os.listdir(UTK_DIR):
    if not img.lower().endswith(('.jpg','.png','.jpeg')):
        continue
    try:
        age = int(img.split("_")[0])
        if age < 18:
            under18_imgs.append(img)
        else:
            adult_imgs.append(img)
    except:
        continue

print(f"Total adult images:    {len(adult_imgs)}")
print(f"Total under-18 images: {len(under18_imgs)}")

# ── Split 80% train / 20% test for each class ─────
def split_and_copy(img_list, train_out, test_out):
    random.shuffle(img_list)
    split = int(len(img_list) * 0.8)
    for img in img_list[:split]:
        shutil.copy(os.path.join(UTK_DIR, img),
                    os.path.join(train_out, img))
    for img in img_list[split:]:
        shutil.copy(os.path.join(UTK_DIR, img),
                    os.path.join(test_out, img))

print("Splitting and copying...")
split_and_copy(adult_imgs,   OUT_TRAIN_ADULT,   OUT_TEST_ADULT)
split_and_copy(under18_imgs, OUT_TRAIN_UNDER18, OUT_TEST_UNDER18)

# ── Summary ────────────────────────────────────────
print("\n===== DONE =====")
print(f"Train adult:    {len(os.listdir(OUT_TRAIN_ADULT))}")
print(f"Train under_18: {len(os.listdir(OUT_TRAIN_UNDER18))}")
print(f"Test adult:     {len(os.listdir(OUT_TEST_ADULT))}")
print(f"Test under_18:  {len(os.listdir(OUT_TEST_UNDER18))}")