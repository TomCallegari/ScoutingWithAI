import pickle

# leagues = ['whl', 'ohl', 'qmjhl']
# leagues_url = [str(i) for i in leagues]

# seasons = ['2001-2002', '2002-2003', '2004-2005',
#             '2005-2006', '2006-2007', '2007-2008', '2008-2009', '2009-2010',
#            '2010-2011', '2011-2012', '2012-2013', '2013-2014', '2014-2015',
#            '2016-2017', '2017-2018', '2018-19']
# seasons_url = [str(i) for i in seasons]

# pages = [str(i) for i in range(1, 5)]

# url_list = []
# for league in leagues_url:
#     for season in seasons_url:
#         for page in pages:
#             url_list.append('http://www.eliteprospects.com/league/' + league + '/stats/' + season + '?sort=tp&page='+ page)

# print(len(url_list))

with open('listfile.data', 'rb') as filehandle:
    urls = pickle.load(filehandle)

print(len(urls))


