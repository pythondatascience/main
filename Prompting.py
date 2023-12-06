# sudo pip3 install pandas

## 파일 설명
# 생성된 csv를 한 데 모아서 하나로 합친 후, openai가 알아듣기 쉽게 내용을 정제하여 txt파일로 출력
# 엉뚱한 답변이나 잘못된 답변을 하지 않게끔 txt 내용을 조절
# 주로 파일 I/O 위주로 사용

## 참조문헌
# ChatGPT : 코드의 대략적인 구조(함수 형태 측면에서)

## 독창적인 부분
# 수업때 배운 pandas를 사용
# GPT가 이해하기 쉽도록 정보를 나열하는 방식(프롬프팅) 알고리즘을 공부한 뒤, 코드화하였음

## 제작방식
# 자체제작(최정민, 정주영)

## Start here (개발담당  : 최정민) - csv 파일을 한데 모아 정제 후 txt 파일로 생성
import pandas as pd

def csv_to_txt(menu_csv_filename, notice_csv_filename, schedule_csv_filename, txt_filename, new_column_order):
    try:
        # CSV 파일을 읽어옴
        menu_df = pd.read_csv(menu_csv_filename)
        notice_df = pd.read_csv(notice_csv_filename)
        schedule1_df = pd.read_csv(schedule_csv_filename)
        schedule2_df = pd.read_csv(schedule_csv_filename)

         # 열 순서 변경
        menu_df = menu_df[new_column_order]
        notice_df = notice_df[6:10]
        notice_df['공지'] = notice_df['공지'].str.replace('새글', '')
        schedule1_df = schedule1_df[:4]
        schedule2_df = schedule2_df[4:]

        ## Start here (개발담당 : 정주영)
        # 기본
        with open(txt_filename, 'w', encoding='utf-8') as f:
            f.write('# 역할\n')
            f.write("너는 'PNU챗봇'이라는 이름을 가지고 있어.\n")
            f.write("너는 부산대 순환버스 위치, 학사일정, 전기과 공지, 금정회관 학식메뉴에 관한 정보를 제공해.\n")
            f.write("너는 '안녕? 반가워!', '뭘 도와줄까?'와 같은 20대 청년의 말투를 사용해.\n\n")
        ## end here (개발담당 : 정주영)

        # 버스
        with open(txt_filename, 'a', encoding='utf-8') as f:
            f.write('<1> 현재 부산대 순환버스 위치.\n')
            f.write('# 순환버스 혹은 금정구7번 버스의 위치에 관해 물어보면 "31qwef#fAWedf#fFsfdew"라고 대답해.\n')
        
        # 학식
        with open(txt_filename, 'a', encoding='utf-8') as f:
            f.write('\n<2> 금정회관 학식 메뉴.\n')
            f.write('# 표의 열은 |으로 구분해 (날짜|타입|식사시간|메뉴).\n')
            f.write('# 질문에는 날짜와 타입에 관한 정보가 반드시 포함되어있어야해.\n')
            f.write(f'# {min(menu_df["날짜"])}와{max(menu_df["날짜"])}에만 정보를 제공해 줘.\n')
            f.write('# 타입은 "1000원의 아침", "일반", "일품"이 있어.\n')
            f.write('# 답변은\n-아침:{메뉴}\n-점심:{메뉴}\n-저녁:{메뉴}의 양식으로 대답해.\n')
            
        menu_df.to_csv(txt_filename, index=False, sep='|', mode='a', encoding='utf-8')
        
        # 공지  
        with open(txt_filename, 'a', encoding='utf-8') as f:   
            f.write('\n<3> 전기공학과 공지.\n')
            f.write('# 표의 열은 |으로 구분해 (작성일|공지).\n')
            
        notice_df.to_csv(txt_filename, index=False, header=False, sep='|', mode='a', encoding='utf-8')
        
        # 학사일정1
        with open(txt_filename, 'a', encoding='utf-8') as f:          
            f.write('\n<4> 1차 학사일정.\n')
            f.write('# 표의 열은 |으로 구분해 (기간|일정).\n# 몇차 학사일정인지 입력을 받을것.\n')

        schedule1_df.to_csv(txt_filename, index=False, header=False, sep='|', mode='a', encoding='utf-8')
        
        # 학사일정2
        with open(txt_filename, 'a', encoding='utf-8') as f:          
            f.write('\n<5> 2차 학사일정.\n')
            f.write('# 표의 열은 |으로 구분해 (기간|일정).\n# 몇차 학사일정인지 입력을 받을것.\n')

        schedule2_df.to_csv(txt_filename, index=False, header=False, sep='|', mode='a', encoding='utf-8')

        print(f"텍스트 파일 {txt_filename}이 생성되었습니다.")

    except Exception as e:
        print(f"오류: {e}")

## end here (개발담당  : 최정민)
