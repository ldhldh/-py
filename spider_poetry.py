from urllib import request
import re
import os
'''
古诗文网 https://www.gushiwen.org/shiwen/
无反爬机制
作者ldhldh
'''
def pr_runtime(func):
    '''
    装饰器：增加运行时间打印
    '''
    import time
    def runtime(*argv, **kw):
        t = time.time()
        func(*argv, **kw)
        print('*******************')
        print(str(time.time() - t) + 's')
    return runtime

class Poetry_gushiwen():
    '''
    古诗文网 https://www.gushiwen.org/shiwen/
    '''
    root_pattern = 'height:22px;"([\s\S]*?)<div class="tool">'
    name_pattern = '<b>([\s\S]*?)</b>'
    author_pattern = '">([\s\S]*?)</a>'
    content_pattern = '<p>([\s\S]*?)</p>'
    content_pattern1 = '">([\s\S]*?)</div>'
    Poetries = []
    def __init__(self, i=None):
        if i == None:
            self.url = 'https://www.gushiwen.org/shiwen'
        else:
            self.url = 'https://www.gushiwen.org/shiwen/default_0AA' + str(i) +'.aspx'
        self.poetries = []
    def __fetch_content(self):
        r = request.urlopen(self.url)
        htmls = r.read()
        htmls = str(htmls, encoding='utf-8')
        return htmls

    def __get_content(self, html):
        content = ''
        html = html.split('id=')[1]
        content1 = re.findall(Poetry_gushiwen.content_pattern, html)
        if not content1:
            content1 = re.findall(Poetry_gushiwen.content_pattern1, html)
        for sentence in content1:
            if '<strong>' in sentence:
                sentence = sentence.replace('<strong>', '')
                sentence = sentence.replace('</strong>', '')
            if '</span>' in sentence and re.findall('</span>([\s\S]*)', sentence):
                content += re.findall('</span>([\s\S]*)', sentence)[0]
            else:
                content += sentence.strip() + '\n'
        return content

    def __analysis(self, htmls):
        root_htmls = re.findall(Poetry_gushiwen.root_pattern, htmls)
        poetries = []
        for html in root_htmls:
            name = re.findall(Poetry_gushiwen.name_pattern, html)[0]
            author = re.findall(Poetry_gushiwen.author_pattern, html.replace('"source">', '"source"'))
            author = author[1] + ' ' + author[2]
            content = self.__get_content(html).replace('<br>', '\n')
            anchor = {'name': name.replace('</span>', ''), 'author': author, 'content': content.replace('<br />', '\n')[:-2]}
            poetries.append(anchor)
        return poetries

    def show_poetry(self, mine=None):
        if mine == None:
            for poetry in self.poetries:
                print('--------')
                print(poetry['name'])
                print(poetry['author'])
                print(poetry['content'])
        else:
            for poetry in Poetry_gushiwen.Poetries:
                print('--------')
                print(poetry['name'])
                print(poetry['author'])
                print(poetry['content'])

    def go(self):
        htmls = self.__fetch_content()
        self.poetries = self.__analysis(htmls)
        Poetry_gushiwen.Poetries += self.poetries
        # self.show_poetry()

    def save_poetries(self, split=None):
        if split == None:
            f = open('poetries.txt', 'w', encoding='utf-8')
            f.write(str(Poetry_gushiwen.Poetries))
            f.close()
        else:
            if not os.path.exists('Poetries'):
                os.mkdir('Poetries')
            files = os.listdir('Poetries')
            for poetry in self.poetries:
                filename = poetry['name'].replace('/', '#') + '.txt'
                if filename in files:
                    continue
                f = open('Poetries/' + filename, 'w', encoding='utf-8')
                f.write(poetry['name'] + '\n' + poetry['author'] + '\n' + poetry['content'].replace('\n\n', '\n').replace('\n\n', '\n'))
                f.close()
        print('saved!')
@pr_runtime
def test():
    for i in range(1, 1000):
        print(i)
        spider = Poetry_gushiwen(i)
        spider.go()
        spider.save_poetries(1)
        # spider.show_poetry()
    save = Poetry_gushiwen()
    save.save_poetries()


if __name__ == '__main__':
    test()

