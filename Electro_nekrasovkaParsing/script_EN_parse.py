import ElectroNekrasokaParser from ElectroNekrasokaParser

VM_1946_1955 = ElectroNekrasokaParser('Vecherniya Moscva', '1', list(range(1946, 1956)))

all_issues_VM = VM_1946_1955.links_to_images(page_num = '4')

all_issues_VM_1946_1955_df = pd.DataFrame(all_issues_VM, columns = ['issue', 'link_to_page', 'link_to_image_with_programme'])

year = all_issues_VM_1946_1955_df['issue'].str.findall(r', ([0-9]{4}),')
date = all_issues_VM_1946_1955_df['issue'].str.findall(r', ([0-9]{1,2} [А-Яа-я]{1,})')

all_issues_VM_1946_1955_df['year'] = year
all_issues_VM_1946_1955_df['date'] = date
all_issues_VM_1946_1955_df['date'] = all_issues_VM_1946_1955_df['date'].apply(lambda x: ''.join(dict.fromkeys(x).keys()))
all_issues_VM_1946_1955_df['year'] = all_issues_VM_1946_1955_df['year'].apply(lambda x: ''.join(dict.fromkeys(x).keys()))

all_issues_VM_1946_1955_df[['day', 'month']] = all_issues_VM_1946_1955_df.date.str.extract(r'([0-9]{1,2}) ([А-Яа-я]{1,})', expand=True)


dict_month = {'января': '1',
              'февраля': '2',
              'марта': '3',
              'апреля': '4',
              'мая': '5',
              'июня': '6',
              'июля': '7',
              'августа': '8',
              'сентября': '9',
              'октября': '10',
              'ноября': '11',
              'декабря': '12'}


all_issues_VM_1946_1955_df = all_issues_VM_1946_1955_df.replace({"month": dict_month})
all_issues_VM_1946_1955_df["year_day"] = all_issues_VM_1946_1955_df["year"] + '/' + all_issues_VM_1946_1955_df["month"] + '/' + all_issues_VM_1946_1955_df["day"]
all_issues_VM_1946_1955_df.drop(['date', 'year', 'day', 'month'], axis=1, inplace=True)

# сохраняем датасет, затем к нему будут присоединена вручную колонка о том, была ли в газете опублкиована киноафиша
# 1 - была, 0 - не была
all_issues_VM_1946_1955_df.to_csv('all_issues_VM_1946_1955_df.csv', sep=',', index=False, encoding='utf-8')
