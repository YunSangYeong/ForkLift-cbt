// Q-Net 종목 7875 시험정보 직접 확인. 영역별 12문항만 앱의 학습용 배분이다.
export const QUALIFICATION = {
  name: "지게차운전기능사",
  title: "지게차운전기능사 필기 CBT",
  bankId: "main",
  storageKey: "forklift-cbt:v1",
  subjects: ["지게차 주행", "화물 적재", "운반", "하역", "안전관리"],
  exam: { questionCount: 60, durationMinutes: 60, choiceCount: 4, passScore: 60,
    maxScore: 100, hasSubjectCutoff: false, perArea: 12 },
  rulesStatus: "verified-summary",
  selectionPolicy: "5개 학습 영역별 12문항: 학습용 균등 배분이며 공식 영역별 출제 수가 아닙니다.",
  rulesNote: "2026-10-20 Q-Net 종목 7875 시험정보 확인: 5개 영역, 4지선다 60문항·60분, 100점 만점에 60점 이상. 과목별 과락 조건은 제시되지 않은 총점 기준입니다. 영역별 출제 수는 공식 자료에서 확인되지 않았습니다.",
} as const;
