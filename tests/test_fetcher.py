from typing import List, Dict
from arxiv_retriever.fetcher import fetch_papers, search_paper_by_title, parse_arxiv_response


def test_parse_arxiv_response():
    """Test parse_arxiv_response function."""
    # mock xml data gotten & modified from section 4.1 of https://info.arxiv.org/help/api/user-manual.htm
    mock_xml = """
    <feed xmlns="http://www.w3.org/2005/Atom" xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/" xmlns:arxiv="http://arxiv.org/schemas/atom">
      <link xmlns="http://www.w3.org/2005/Atom" href="http://arxiv.org/api/query?search_query=all:electron&amp;id_list=&amp;start=0&amp;max_results=1" rel="self" type="application/atom+xml"/>
      <title xmlns="http://www.w3.org/2005/Atom">ArXiv Query: search_query=all:electron&amp;id_list=&amp;start=0&amp;max_results=1</title>
      <updated xmlns="http://www.w3.org/2005/Atom">2007-10-08T00:00:00-04:00</updated>
      <opensearch:totalResults xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">1000</opensearch:totalResults>
      <entry xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
        <id xmlns="http://www.w3.org/2005/Atom">http://arxiv.org/abs/hep-ex/0307015</id>
        <published xmlns="http://www.w3.org/2005/Atom">2003-07-07T13:46:39-04:00</published>
        <title xmlns="http://www.w3.org/2005/Atom">Multi-Electron Production at High Transverse Momenta in ep Collisions at HERA</title>
        <summary xmlns="http://www.w3.org/2005/Atom">Multi-electron production is studied at high electron transverse 
        momentum in positron- and electron-proton collisions using the H1 detector at HERA. The data correspond to an 
        integrated luminosity of 115 pb-1.
        </summary>
        <author xmlns="http://www.w3.org/2005/Atom">
          <name xmlns="http://www.w3.org/2005/Atom">H1 Collaboration</name>
        </author>
      </entry>
    </feed>
    """

    result = parse_arxiv_response(mock_xml)
    assert len(result) == 1
    assert isinstance(result, List) and isinstance(result[0], Dict)  # returns expected type
    assert result[0]['title'] == 'Multi-Electron Production at High Transverse Momenta in ep Collisions at HERA'
    assert result[0]['authors'] == ['H1 Collaboration']

