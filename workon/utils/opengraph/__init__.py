# encoding: utf-8

import os, re, requests
import lxml.html
import workon.utils

def opengraph(url):
    metadata = {}
    url = workon.utils.append_protocol(url)
    try:
        r = requests.get(url)
    except requests.ConnectionError:
        return metadata


    base_url = "/".join(r.url.split('/')[0:3])

    # print 'GET ', url, r.status_code, r.content
    content = ""
    head = ""
    i = 0
    s = -1
    e = -1
    for chunk in r.iter_content(chunk_size=512):
        if chunk:
            content += chunk
            if s != -1:
                e = chunk.find('</head>')
                if e != -1:
                    e += i
                    head = content[s:e+7]
                    break
            else:
                s = chunk.find('<head')
                if s != -1:
                    s += i
            i += len(chunk)

    if head:
        html = lxml.html.fromstring(head)

        metadata['url'] = url

        metadata['title'] = html.xpath('//meta[@property="og:title"]/@content')
        metadata['title'] += html.xpath('//title/text()')

        metadata['site_name'] = html.xpath('//meta[@property="og:site_name"]/@content')
        metadata['site_name'] += [base_url]

        metadata['icon'] = html.xpath('//link[@rel="icon"]/@href')
        metadata['icon'] += html.xpath('//link[@rel="shortcut icon"]/@href')
        metadata['icon'] += html.xpath('//link[@rel="favicon"]/@href')
        for i, icon in enumerate(metadata['icon']):
            if icon.startswith('/'):
                metadata['icon'][i] = base_url + icon

        if not metadata['icon']:
            default_favicon = base_url +'/favicon.ico'
            if requests.head(default_favicon).status_code == 200:
                metadata['icon'] += [default_favicon]

        metadata['keywords'] = html.xpath('//meta[@property="og:keywords"]/@content')
        metadata['keywords'] += html.xpath('//meta[@name="keywords"]/@content')
        metadata['keywords'] += html.xpath('//meta[@name="Keywords"]/@content')

        metadata['description'] = html.xpath('//meta[@property="og:description"]/@content')
        metadata['description'] += html.xpath('//meta[@name="description"]/@content')
        metadata['description'] += html.xpath('//meta[@name="Description"]/@content')

        metadata['image'] = html.xpath('//meta[@property="og:image"]/@content')
        metadata['image'] += html.xpath('//link[@rel="image_src"]/@href')

    return metadata