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


dict_month = {'1': 'января',
              '2': 'февраля',
              '3': 'марта',
              '4': 'апреля',
              '5': 'мая',
              '6': 'июня',
              '7': 'июля',
              '8': 'августа',
              '9': 'сентября',
              '10': 'октября',
              '11': 'ноября',
              '12': 'декабря'}


all_issues_VM_1946_1955_df = all_issues_VM_1946_1955_df.replace({"month": dict_month})
all_issues_VM_1946_1955_df["year_day"] = all_issues_VM_1946_1955_df["year"] + '/' + all_issues_VM_1946_1955_df["month"] + '/' + all_issues_VM_1946_1955_df["day"]
all_issues_VM_1946_1955_df.drop(['date', 'year', 'day', 'month'], axis=1, inplace=True)

all_issues_VM_1946_1955_df.to_csv('all_issues_VM_1946_1955_df.csv', sep=',', index=False, encoding='utf-8')
