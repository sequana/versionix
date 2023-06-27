from versionix.parser import get_version




def test_version():

    assert get_version("ls")
    assert get_version("singularity")


    # stable versions can be checked 
    assert  get_version("bwa") == "0.7.17-r1188"
    assert  get_version("bedtools").startswith("v2")
