"""Testing test discovery

"""

import os
import zenunit as zu

def test_discover():
    """Discover tests

    """

    dirname = os.path.dirname(__file__)
    test_result = zu.runtest(os.path.join(dirname, 'sample1'), mode='unit')

    assert len(test_result) > 1
