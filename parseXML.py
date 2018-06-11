import json
import os
import os.path as op
import re
from gzip import GzipFile

from bs4 import BeautifulSoup

DATA_FOLDER = 'data'


def getallfiles(path):
    return [op.join(dp, fn) for dp, dn, fns in os.walk(path) for fn in fns if fn.endswith('gz')]


def process_front(front):
    to_return = {}

    jm = front.find('journal-meta')
    journal_meta = {}
    journal_meta['journal_ids'] = [jid.string for jid in
                                   jm.find_all('journal-id')]
    journal_meta['journal_title'] = jm.find('journal-title').get_text()
    journal_meta['issns'] = {issn['pub-type']: issn.string for issn in jm.find_all('issn')}
    journal_meta['publisher'] = {publ.name.split('publisher-')[1]: publ.string for publ in
                                 jm.find_all(re.compile('publisher-.*'))}

    to_return['journal_meta'] = journal_meta

    am = front.find('article-meta')
    article_meta = {}
    article_meta['article_ids'] = [aid.string for aid in
                                   am.find_all('article-id')]
    article_meta['subject'] = am.subject.string
    article_meta['article_title'] = getstring(am.find('article-title'))
    article_meta['authors'] = [
        {'surname': getstring(aut.surname), 'given_name': getstring(aut.find('given-names')),
         # 'initials': ' '.join(list(map(lambda x: '%s.' % x[0], aut.find('given-names').string.split(' ')))),
         'corresp': True if aut.get('corresp') is not None else False,
         'aff': [aff['rid'] for aff in aut.find_all('xref', {'ref-type': 'aff'})]} for aut
        in am.find_all('contrib', {'contrib-type': 'author'})]

    # TODO: o sa crape pe unele, check
    # article_meta['aff'] = {aff['id']: {'institution': ' '.join(map(lambda x: x.get_text(), aff.find_all('institution'))),
    #                                    'country': getstring(aff.country), 'address': aff.get_text()} for aff in
    #                        am.find_all('aff', id=True)}
    # if len(article_meta['aff']) == 1:
    #     affval = list(iter(article_meta['aff']))[0]
    #     for aut in article_meta['authors']:
    #         if not aut['aff']:
    #             aut['aff'].append(affval)
    article_meta['pub_data'] = {
        pd.get('pub-type', pd.get('date-type')): {child.name: getint(child) for child in pd.children if child != '\n'}
        for pd in am.find_all('pub-date')
    }
    article_meta['counts'] = {'ref_count': am.find('ref-count')['count'] if am.find('ref-count') is not None else None}
    article_meta['volume'] = getint(am.volume)
    article_meta['issue'] = getint(am.issue)
    # TODO: rewrite funding
    # article_meta['funding'] = {
    #     award.find('award-id').string: {'institution': award.institution.string, 'surname': award.surname.string,
    #                                     'given_name': award.find('given-name')} for award in am.find_all('award-group')
    # }

    to_return['article_meta'] = article_meta
    # print(json.dumps(to_return, indent=3))
    return to_return


def getstring(tag):
    itags = ['italic', 'bold']
    try:
        for itag in itags:
            for x in tag.find_all(itag):
                x.unwrap()
        return ''.join(tag.find_all(text=True, recursive=False))
    except:
        return ''


def getint(tag):
    try:
        return int(getstring(tag))
    except:
        return None


def process_back(back):
    to_return = {}
    # ref_list = {ref['id']: {
    #     'pub_type': ref.find('mixed-citation')['publication-type'],
    #     'authors': [{'surname': getstring(aut.surname), 'given_name': getstring(aut.find('given-names'))} for aut in
    #                 ref.find_all('name')],
    #     'year': ref.year.string,
    #     'article_title': ref.find('article-title').get_text() if ref.find('article-title') is not None else None,
    #     'article_ids': {aid['pub-id-type'].replace('-', '_'): aid.string for aid in
    #                     ref.find_all('pub-id')}
    # } for ref in back.find_all('ref')}

    ref_list = []
    for ref in back.find_all('ref'):
        ref_data = {}
        ref_list.append(ref_data)

        mc = ref.find('mixed-citation')
        if mc is None:
            mc = ref.find('element-citation')
        pub_type = mc['publication-type'] if mc is not None else None
        ref_data['pub_type'] = pub_type

        if pub_type == 'other':
            ref_data['article_title'] = mc.get_text()
            continue

        ref_data['article_title'] = getstring(ref.find('article-title'))
        authors = []
        for aut in ref.find_all('name'):
            authors.append({'surname': getstring(aut.surname), 'given_name': getstring(aut.find('given-names'))})
        ref_data['authors'] = authors

        ref_data['source'] = getstring(ref.source)
        ref_data['year'] = getint(ref.year)
        ref_data['volume'] = getint(ref.volume)
        ref_data['issue'] = getint(ref.issue)

        ref_data['publisher'] = {publish_tag.name.split('publisher-')[1]: publish_tag.get_text() for publish_tag in
                                 ref.find_all(re.compile('publisher-.*'))}

        ref_data['referred_article_ids'] = [aid.string for aid in
                                   ref.find_all('pub-id')]

    to_return['ref_list'] = ref_list
    # print(json.dumps(ref_list, indent=3))

    return to_return


def processXML(xmlfile):
    to_return = []
    soup = BeautifulSoup(GzipFile(xmlfile, 'r'), 'lxml', from_encoding='utf-8')
    # print(soup)
    for record in soup.find_all('record'):
        print(record.header.identifier.string)
        record_data = {'front': process_front(record.front), 'back': process_back(record.back)}
        to_return.append(record_data)
        # break
    # print(json.dumps(to_return, indent=3))
    # json.dump(to_return, open('test.json', 'w'), indent=3)
    return to_return


def main():
    for xml in getallfiles(DATA_FOLDER):
        print('Processing : %s' % xml)
        json.dump(processXML(xml), open(xml.split('.')[0] + '.json', 'w', encoding='utf8'),
                  ensure_ascii=False)
        # break


if __name__ == '__main__':
    main()
