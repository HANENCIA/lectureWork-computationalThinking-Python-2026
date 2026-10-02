from __future__ import annotations

import sys
from pathlib import Path

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import numpy as np
import pandas as pd
from PIL import Image, ImageTk
from wordcloud import ImageColorGenerator, WordCloud

# 설정값: 프로그램 전체에서 공통으로 사용하는 기본값
WINDOW_TITLE = "CSV 기반 워드클라우드 생성기 (컴퓨팅사고 교육용)"
PREVIEW_WIDTH = 900  # 미리보기에서 표시할 Wordcloud 가로 길이
PREVIEW_HEIGHT = 650  # 미리보기에서 표시할 Wordcloud 세로 길이


# 파일 선택 함수: CSV
def select_csv_file() -> str:
    return filedialog.askopenfilename(title="단어 빈도 CSV 파일 선택", filetypes=[("CSV 파일", "*.csv")])


# 파일 선택 함수: 배경(마스크) 이미지
def select_mask_image() -> str:
    return filedialog.askopenfilename(title="배경(마스크) 이미지 선택", filetypes=[("이미지 파일", "*.png *.jpg *.jpeg *.bmp")])


# CSV에서 불러와서 단어 빈도 데이터 처리
def load_word_frequencies(csv_path: str) -> dict[str, int]:
    # 1. CSV 파일 경로 지정 확인: 경로를 지정하였는지 확인하고 CSV 파일을 선택하지 않았을 경우 에러 반환
    if not csv_path:
        raise ValueError("CSV 파일을 선택하지 않았습니다.")

    # 2. CSV 파일 불러오기: 여기서 header=None을 함으로써 첫 번째 행은 읽지 않고 무시함)
    data = pd.read_csv(csv_path, sep=",", encoding="utf-8", header=None)

    # 3. CSV 파일 확인: 만약 CSV가 최소 2개의 열(Column)으로 구성되어 있지 않을 경우 에러 반환
    if data.shape[1] < 2:
        raise ValueError("CSV에는 최소 2개의 열(단어, 빈도)이 필요합니다.")

    # 4. 빈도 데이터를 변환할 Dict 초기화
    frequencies: dict[str, int] = {}

    # 5. 한 행(row)씩 읽어가면서 처리, 단 열 2개만 사용
    for word, frequency in data.iloc[:, :2].itertuples(index=False):
        # 6. 단어 앞, 뒤 공백 제거
        word = str(word).strip()
        # 7. 단어가 word, 단어, term이거나 공백인 경우에는 제외
        if not word or word.lower() in {"word", "단어", "term"}:
            continue

        # 8. frequency 점검: 숫자가 아니면 에러 발생
        try:
            frequency = int(frequency)
        except (TypeError, ValueError) as error:
            raise ValueError(f"빈도 값은 숫자여야 합니다: {word} -> {frequency}") from error

        # 9. frequency가 음수일 경우 무시
        if frequency <= 0:
            continue

        # 10. 단어별 빈도를 누적 합산
        frequencies[word] = frequencies.get(word, 0) + frequency

    # 11. 최종 점검: 필터링 후 유효한 단어가 하나도 없으면 오류를 발생
    if not frequencies:
        raise ValueError("사용할 수 있는 단어와 양의 빈도 값이 없습니다.")

    return frequencies


# 배경(마스크) 이미지 불러오기
def load_mask_image(image_path: str) -> np.ndarray:
    if not image_path:
        raise ValueError("마스크 이미지를 선택하지 않았습니다.")

    image = Image.open(image_path).convert("RGB")
    return np.array(image)

# 워드 클라우드 폰트 경로 관ㄹ
def resource_path(relative_path: str) -> str:
    """PyInstaller packaged exe 에서도 자원 파일 경로를 올바르게 반환."""
    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).parent
    return str(base_path / relative_path)


# 워드 클라우드 만들기
def create_wordcloud(frequencies: dict[str, int], mask: np.ndarray) -> WordCloud:
    color_generator = ImageColorGenerator(mask)

    wordcloud = WordCloud(
        font_path=resource_path("./res/fonts/08SeoulNamsanB.ttf"),
        width=800,
        height=600,
        min_font_size=20,
        max_font_size=200,
        background_color="rgba(255, 255, 255, 0)",
        mode="RGBA",
        mask=mask,
        collocations=False,
    )

    wordcloud.generate_from_frequencies(frequencies)
    wordcloud.recolor(color_func=color_generator)
    return wordcloud


# 미리보기
def show_wordcloud(wordcloud: WordCloud, preview_label: ttk.Label) -> None:
    image = wordcloud.to_image().convert("RGBA")
    image.thumbnail((PREVIEW_WIDTH, PREVIEW_HEIGHT))

    preview_photo = ImageTk.PhotoImage(image)
    preview_label.configure(image=preview_photo, text="")
    preview_label.image = preview_photo


# 저장
def save_wordcloud(wordcloud: WordCloud | None) -> None:
    if wordcloud is None:
        messagebox.showwarning("저장할 결과 없음", "먼저 워드클라우드를 생성하세요.")
        return

    save_path = filedialog.asksaveasfilename(
        title="워드클라우드 저장",
        defaultextension=".png",
        filetypes=[("PNG 이미지", "*.png")],
    )

    if not save_path:
        return

    try:
        wordcloud.to_file(save_path)
        messagebox.showinfo("저장 완료", f"워드클라우드를 저장했습니다.\n{save_path}")
    except Exception as error:
        messagebox.showerror("저장 오류", f"파일을 저장하지 못했습니다.\n{error}")


# GUI
class WordCloudApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry("1100x850")
        self.root.minsize(800, 650)

        self.current_wordcloud: WordCloud | None = None
        self.csv_path = tk.StringVar(value="선택된 CSV 파일 없음")
        self.image_path = tk.StringVar(value="선택된 마스크 이미지 없음")
        self.status = tk.StringVar(value="CSV와 마스크 이미지를 선택하세요.")

        self.build_widgets()

    def build_widgets(self) -> None:
        control_frame = ttk.Frame(self.root, padding=12)
        control_frame.pack(fill="x")

        ttk.Button(control_frame,
                   text="CSV 선택",
                   command=self.on_select_csv).grid(row=0, column=0, padx=4, pady=4, sticky="ew")

        ttk.Label(control_frame,
                  textvariable=self.csv_path,
                  width=80).grid(row=0, column=1, padx=4, pady=4, sticky="ew")

        ttk.Button(control_frame,
                   text="마스크 이미지 선택",
                   command=self.on_select_image).grid(row=1, column=0, padx=4, pady=4, sticky="ew")

        ttk.Label(control_frame,
                  textvariable=self.image_path,
                  width=80).grid(row=1, column=1, padx=4, pady=4, sticky="ew")

        ttk.Button(control_frame,
                   text="워드클라우드 생성",
                   command=self.on_generate).grid(row=2, column=0, padx=4, pady=8, sticky="ew")

        ttk.Button(control_frame,
                   text="결과 저장",
                   command=self.on_save).grid(row=2, column=1, padx=4, pady=8, sticky="w")

        control_frame.columnconfigure(1, weight=1)

        ttk.Separator(self.root, orient="horizontal").pack(fill="x")

        self.preview_label = ttk.Label(self.root,
                                       text="생성된 워드클라우드가 여기에 표시됩니다.",
                                       anchor="center")
        self.preview_label.pack(fill="both", expand=True, padx=12, pady=12)

        ttk.Label(self.root,
                  textvariable=self.status,
                  relief="sunken",
                  anchor="w",
                  padding=5).pack(fill="x", side="bottom")

    def on_select_csv(self) -> None:
        selected_path = select_csv_file()
        if selected_path:
            self.csv_path.set(selected_path)
            self.status.set("CSV 파일을 선택했습니다.")

    def on_select_image(self) -> None:
        selected_path = select_mask_image()
        if selected_path:
            self.image_path.set(selected_path)
            self.status.set("마스크 이미지를 선택했습니다.")

    def on_generate(self) -> None:
        try:
            frequencies = load_word_frequencies(self.csv_path.get())
            mask = load_mask_image(self.image_path.get())
            self.current_wordcloud = create_wordcloud(frequencies, mask)
            show_wordcloud(self.current_wordcloud, self.preview_label)
            self.status.set(f"생성 완료: {len(frequencies)}개 단어")
        except Exception as error:
            self.current_wordcloud = None
            self.status.set("생성 중 오류가 발생했습니다.")
            messagebox.showerror("워드클라우드 생성 오류", str(error))

    def on_save(self) -> None:
        save_wordcloud(self.current_wordcloud)


def main() -> None:
    root = tk.Tk()
    WordCloudApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
