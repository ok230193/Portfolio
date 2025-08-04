import cv2
import matplotlib.pyplot as plt
import copy
import numpy as np
import torch
import time

from src import model
from src import util
from src.body import Body
from src.hand import Hand

body_estimation = Body('model/body_pose_model.pth')
hand_estimation = Hand('model/hand_pose_model.pth')

print(f"Torch device: {torch.cuda.get_device_name()}")

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

window_name = 'demo'

# ウィンドウをリサイズ可能に設定
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

# ウィンドウのサイズを設定
cv2.resizeWindow(window_name, 1280, 720)

# 各人物のHPを保持するリスト
hp_list = [5, 5]

# 各人物の攻撃状態を保持するリスト
previous_attack_states = [False, False]


# インデックスが有効かどうかを確認する関数
def valid_index(index, size):
    return 0 <= index < size


# 攻撃モーションを検出する関数
def attack_motion(candidate, person):
    r_shoulder_index = int(person[2])
    r_wrist_index = int(person[4])
    if valid_index(r_shoulder_index, len(candidate)) and valid_index(r_wrist_index, len(candidate)):
        r_shoulder = candidate[r_shoulder_index, 0:2]
        r_wrist = candidate[r_wrist_index, 0:2]
        if r_wrist[1] < r_shoulder[1]:
            return True
    return False


# 防御モーションを検出する関数
def defense_motion(candidate, person):
    l_hip_index = int(person[11])
    r_hip_index = int(person[8])
    if valid_index(l_hip_index, len(candidate)) and valid_index(r_hip_index, len(candidate)):
        l_hip = candidate[l_hip_index, 0:2]
        r_hip = candidate[r_hip_index, 0:2]
        mid_hip = (l_hip + r_hip) / 2
        if mid_hip[1] > 400:
            return True
    return False


# ゲーム終了を検出する関数
def check_game_over(hp_list):
    if hp_list[0] <= 0:
        return 1
    elif hp_list[1] <= 0:
        return 0
    return -1


while True:
    ret, oriImg = cap.read()
    candidate, subset = body_estimation(oriImg)
    canvas = copy.deepcopy(oriImg)

    # 手を検出する
    hands_list = util.handDetect(candidate, subset, oriImg)

    all_hand_peaks = []
    for x, y, w, is_left in hands_list:
        peaks = hand_estimation(oriImg[y:y+w, x:x+w, :])
        peaks[:, 0] = np.where(peaks[:, 0] == 0, peaks[:, 0], peaks[:, 0]+x)
        peaks[:, 1] = np.where(peaks[:, 1] == 0, peaks[:, 1], peaks[:, 1]+y)
        all_hand_peaks.append(peaks)

    # 2人以上の人物が検出されている場合のみ、HPを更新
    if len(subset) >= 2:
        # 左右の人物を区別する
        subset = sorted(subset[:2], key=lambda x: candidate[int(x[0]), 0])  # 左右の人物を区別

        left_person = subset[0]
        right_person = subset[1]

        # 攻撃と防御の判定
        for i, person in enumerate([left_person, right_person]):
            current_attack_state = attack_motion(candidate, person)

            if current_attack_state and not previous_attack_states[i]:
                # 相手の防御状態をチェック
                target_person_index = (i + 1) % 2
                target_person = [left_person, right_person][target_person_index]
                if not defense_motion(candidate, target_person):
                    hp_list[target_person_index] -= 1

            # 現在の攻撃状態を保持
            previous_attack_states[i] = current_attack_state

        # HPを表示
        for i, person in enumerate([left_person, right_person]):
            head_index = int(person[0])
            if valid_index(head_index, len(candidate)):
                head_pos = candidate[head_index, 0:2]
                cv2.putText(canvas, f'HP: {hp_list[i]}', (int(head_pos[0]), int(head_pos[1] - 20)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # 攻撃と防御の状態を表示
        for i, person in enumerate([left_person, right_person]):
            if attack_motion(candidate, person):
                cv2.putText(canvas, f'Person {i+1}: Attack', (50, 50 + 50*i), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            if defense_motion(candidate, person):
                cv2.putText(canvas, f'Person {i+1}: Defense', (50, 100 + 50*i), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    # ゲームオーバーのチェック
    game_over = check_game_over(hp_list)
    if game_over != -1:
        cv2.putText(canvas, f'Person {game_over + 1} Wins!', (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 3, cv2.LINE_AA)
        cv2.imshow(window_name, canvas)
        cv2.waitKey(3000)  # 3秒待つ
        break

    cv2.imshow(window_name, canvas)  # ビデオを表示するウィンドウ

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
