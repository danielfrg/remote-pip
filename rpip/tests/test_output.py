from rpip.output import Output

exit0 = {'exit_code': 0, 'stdout': 'yes', 'stderr': ''}
exit1 = {'exit_code': 1, 'stdout': '', 'stderr': 'ERROR'}

o0 = {'host1': exit0, 'host2': exit0, 'host3': exit0}
o1 = {'host1': exit0, 'host2': exit1, 'host3': exit0}
o2 = {'host1': exit0, 'host2': exit1, 'host3': exit1}


def test_groupby():
    o = Output(o0)
    groups = o.groupby()
    assert len(groups) == 1

    nodes, output = groups[0]
    assert len(nodes) == 3
    assert nodes == ['host3', 'host2', 'host1']
    assert output == exit0


def test_groupby2():
    o = Output(o1)
    groups = o.groupby()
    assert len(groups) == 2

    nodes, output = groups[0]
    assert len(nodes) == 2
    assert nodes == ['host3', 'host1']
    assert output == exit0

    nodes, output = groups[1]
    assert len(nodes) == 1
    assert nodes == ['host2']
    assert output == exit1


def test_groupby3():
    o = Output(o2)
    groups = o.groupby()
    assert len(groups) == 2

    nodes, output = groups[0]
    assert len(nodes) == 2
    assert nodes == ['host3', 'host2']
    assert output == exit1

    nodes, output = groups[1]
    assert len(nodes) == 1
    assert nodes == ['host1']
    assert output == exit0
