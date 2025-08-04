import glob
import cv2
import os
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import time

# メッセージの表示遅延設定
INITIAL_DELAY = 1.5  # キャラクターが映った後の初期遅延時間（秒）
MESSAGE_INTERVAL = 3  # 各メッセージの表示間隔（秒）

# グローバル設定
FONT_PATH = "C:/Windows/Fonts/meiryo.ttc"  # 日本語フォントのパス
FONT_SIZE_SMALL = 20
WINDOW_SIZE = (1600, 800)
ANIMATION_FOLDERS = {
    1: {
        0: r"C:\Users\ok230193\Documents\L2\babu_",
        80: r"C:\Users\ok230193\Documents\L2\idou",
    },
    4: {
        "不安全": r"C:\Users\ok230193\Documents\L2\tameiki",
        "安全": r"C:\Users\ok230193\Documents\L2\yorokobi",
    }
}

# マーカー状態の初期設定
levels = {1: 0, 2: 0, 3: 0, 4: "不安全"}
count = {1: 0, 2: 0, 3: 0, 4: 0}
coins = 100  # 初期コイン数の設定
coin_increase_flag = False  # 目標達成で一度だけコインを増やすためのフラグ

# ArUco辞書とパラメータ設定
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_1000)
parameters = cv2.aruco.DetectorParameters()

# マーカーごとのメッセージ辞書
marker_messages = {
    1: {
        0: [
            "ここは分電盤の点検でちゅ",
            "ベテランの作業員は○○から点検してるでちゅ",
            "ここでの作業目安時間は△△分でちゅ",
            "今日も安全に点検するでちゅ"
        ],
        80: [
            "さあ、今日も頑張ろう！",
            "今日の目標は、指さし確認を徹底するだよ！",
            "目標達成目指して頑張ろう！！",
            "いいね！指さし完璧！目標達成！"
        ]
    },
    4: {
        "安全": [
            "ここは、送風機の点検だよ！",
            "ここでは、送風機の電源は切ってから始めようね！",
            "送風機の電源を切らないと、指を切っちゃうよ！",
            "いいね！ちゃんと送風機の電源を切ってできてるね！"
        ],
        "不安全": [
            "ここは、送風機の点検だよ！",
            "危ない！！",
            "まずは電源をしっかり切ってから始めてね",
            "安全第一だよ！"
        ]
    }
}

def load_animation_frames():
    frames = {1: {}, 2: {}, 3: {}, 4: {}}
    for marker_id, levels_dict in ANIMATION_FOLDERS.items():
        for level_or_state, folder in levels_dict.items():
            frame_files = sorted(glob.glob(os.path.join(folder, '*.png')))
            frames[marker_id][level_or_state] = frame_files
    return frames

def initialize_camera():
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("AR Camera", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("AR Camera", *WINDOW_SIZE)
    return cap

def draw_speech_bubble(draw, x, y, text, font):
    text_bbox = draw.textbbox((x, y), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    bubble_padding = 10
    bubble_rect = [x - bubble_padding, y - bubble_padding, x + text_width + bubble_padding,
                   y + text_height + bubble_padding]
    draw.rectangle(bubble_rect, fill="white", outline="black")
    draw.text((x, y), text, font=font, fill="black")

coin_increase_flags = {1: False, 2: False, 3: False, 4: False}  # マーカーごとのフラグ

# グローバル変数にコイン獲得メッセージの表示時間を記録する変数を追加
coin_increase_flags = {1: False, 2: False, 3: False, 4: False}  # マーカーごとのフラグ
coin_message_start_time = {1: None, 2: None, 3: None, 4: None}  # マーカーごとのメッセージ表示開始時間

def draw_text(frame_pil, detected_ids, small_font, corners, message_indices, speaking_flags):
    global coins  # グローバル変数 coins を使用する宣言
    draw = ImageDraw.Draw(frame_pil)

    for i, marker_id in enumerate(detected_ids):
        corner = corners[i][0]
        x, y = int(corner[0][0]) - 150, int(corner[0][1]) - 50

        if marker_id in marker_messages and speaking_flags.get(marker_id, False):
            level_or_state = levels.get(marker_id)
            messages = marker_messages[marker_id].get(level_or_state, [])
            current_message_index = message_indices[marker_id]
            message = messages[current_message_index % len(messages)]

            if "危ない！！" in message:
                large_font = ImageFont.truetype(FONT_PATH, 100)
                danger_text = "危ない！！"
                remaining_message = message.replace("危ない！！", "")
                draw.text((x, y), danger_text, font=large_font, fill="red")
                draw.text((x, y + 45), remaining_message, font=small_font, fill="black")
            elif "目標達成！" in message or "いいね！ちゃんと送風機の電源を切ってできてるね" in message:
                # コイン獲得メッセージを2秒間表示するロジック
                if not coin_increase_flags[marker_id]:
                    coins += 10
                    coin_increase_flags[marker_id] = True
                    large_font = ImageFont.truetype(FONT_PATH, 60)
                    draw.text((x, y - 100), "10コイン獲得！", font=large_font, fill="gold")
                    coin_message_start_time[marker_id] = time.time()  # メッセージ開始時間を記録

                # 2秒間メッセージを表示する
                elif time.time() - coin_message_start_time[marker_id] < 2:
                    large_font = ImageFont.truetype(FONT_PATH, 60)
                    draw.text((x, y - 100), "10コイン獲得！", font=large_font, fill="gold")

                draw_speech_bubble(draw, x, y, message, small_font)
            else:
                draw_speech_bubble(draw, x, y, message, small_font)

def draw_overlay_info(draw, level, coins, font):
    draw.rectangle([(10, 10), (110, 40)], fill="white")
    draw.text((10, 10), f"レベル: {level}", font=font, fill="black")
    draw.rectangle([(500, 10), (615, 40)], fill="white")
    draw.text((500, 10), f"コイン: {coins}", font=font, fill="black")

def overlay_animation(frame, x, y, marker_width, marker_height, animation_frame):
    resized_frame = cv2.resize(animation_frame, (marker_width, marker_height))
    alpha_channel = resized_frame[:, :, 3]
    rgb_channels = resized_frame[:, :, :3]
    mask = alpha_channel == 255
    for c in range(3):
        frame[y:y + marker_height, x:x + marker_width, c] = np.where(mask, rgb_channels[:, :, c],
                                                                     frame[y:y + marker_height, x:x + marker_width, c])

def main():
    animation_frames = load_animation_frames()
    frame_counters = {1: 0, 2: 0, 3: 0, 4: 0}
    message_indices = {1: 0, 2: 0, 3: 0, 4: 0}
    last_message_update_times = {}
    message_start_times = {}
    speaking_flags = {1: False, 2: False, 3: False, 4: False}

    cap = initialize_camera()
    small_font = ImageFont.truetype(FONT_PATH, FONT_SIZE_SMALL)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        detected_ids = set(ids.flatten()) if ids is not None else set()

        for marker_id in detected_ids:
            if marker_id not in message_start_times:
                message_start_times[marker_id] = time.time()
                message_indices[marker_id] = 0
                last_message_update_times[marker_id] = time.time()
                speaking_flags[marker_id] = False

        key = cv2.waitKey(1) & 0xFF
        if key == ord('a'):
            for marker_id in detected_ids:
                if marker_id == 1:
                    levels[marker_id] = 80
                elif marker_id == 4:
                    levels[marker_id] = "安全"
        elif key == ord('b'):
            for marker_id in detected_ids:
                if marker_id == 1:
                    levels[marker_id] = 0
                elif marker_id == 4:
                    levels[marker_id] = "不安全"
        elif key == ord('r'):
            for marker_id in detected_ids:
                speaking_flags[marker_id] = True
                message_indices[marker_id] = 0
                message_start_times[marker_id] = time.time()
                last_message_update_times[marker_id] = time.time()
                frame_counters[marker_id] = 0
                coin_increase_flags[marker_id] = False
        elif key == ord('q'):
            break

        for marker_id in detected_ids:
            if marker_id in marker_messages and speaking_flags.get(marker_id, False):
                if time.time() - message_start_times.get(marker_id, 0) > INITIAL_DELAY:
                    if time.time() - last_message_update_times[marker_id] > MESSAGE_INTERVAL:
                        message_indices[marker_id] += 1
                        last_message_update_times[marker_id] = time.time()
                        if message_indices[marker_id] >= len(marker_messages[marker_id].get(levels[marker_id], [])):
                            speaking_flags[marker_id] = False

        if ids is not None:
            for i, marker_id in enumerate(ids.flatten()):
                if marker_id in animation_frames and levels[marker_id] in animation_frames[marker_id]:
                    corner = corners[i][0]
                    x, y = int(corner[0][0]), int(corner[0][1])
                    marker_width = int(corner[1][0] - corner[0][0])
                    marker_height = int(corner[2][1] - corner[0][1])

                    current_level_or_state = levels[marker_id]
                    current_frames = animation_frames[marker_id][current_level_or_state]

                    if speaking_flags.get(marker_id, False):
                        animation_frame = cv2.imread(current_frames[frame_counters[marker_id] % len(current_frames)],
                                                     cv2.IMREAD_UNCHANGED)
                        frame_counters[marker_id] += 1
                    else:
                        animation_frame = cv2.imread(current_frames[0], cv2.IMREAD_UNCHANGED)

                    if animation_frame is not None and animation_frame.shape[2] == 4:
                        overlay_animation(frame, x, y, marker_width, marker_height, animation_frame)

        frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw_text(frame_pil, detected_ids, small_font, corners, message_indices, speaking_flags)
        draw_overlay_info(ImageDraw.Draw(frame_pil), levels[1], coins, small_font)

        frame = cv2.cvtColor(np.array(frame_pil), cv2.COLOR_RGB2BGR)
        cv2.imshow('AR Camera', frame)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
