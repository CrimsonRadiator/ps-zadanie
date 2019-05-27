import pytest
import datahandler
import controller

@pytest.fixture()
def data_handler():
    dh = datahandler.DataHandler()
    return dh

@pytest.fixture()
def ctl():
    ctl = controller.Controller()
    return ctl



v_list = ['Dolnośląskie',
          'Kujawsko-pomorskie',
          'Lubelskie',
          'Lubuskie',
          'Łódzkie',
          'Małopolskie',
          'Mazowieckie',
          'Opolskie',
          'Podkarpackie',
          'Podlaskie',
          'Pomorskie',
          'Śląskie',
          'Świętokrzyskie',
          'Warmińsko-Mazurskie',
          'Wielkopolskie',
          'Zachodniopomorskie']

v_yearly = ['2010 81.65%',
           '2011 74.60%',
           '2012 80.30%',
           '2013 80.80%',
           '2014 71.03%',
           '2015 73.21%',
           '2016 79.45%',
           '2017 78.12%',
           '2018 77.44%']

v_compare =['2010 Pomorskie           81.65%',
            '2011 Podlaskie           76.77%',
            '2012 Podlaskie           81.73%',
            '2013 Podlaskie           81.83%',
            '2014 Podlaskie           72.90%',
            '2015 Podlaskie           75.45%',
            '2016 Podlaskie           80.89%',
            '2017 Podlaskie           80.42%',
            '2018 Podlaskie           81.19%']

def test_database_existance(data_handler):
    assert data_handler.raw_select("SELECT name FROM sqlite_master WHERE type='table' AND name='matura'") is not None

def test_database_record_count(data_handler):
    assert data_handler.raw_select("SELECT COUNT(*) FROM matura")[0][0] == 576

def test_controller_voivodeships(ctl):
    for v in v_list:
        assert ctl.calculate_mean(v, 2018) is not None

def test_controller_mean(ctl):
    val = '{:.2f}'.format(ctl.calculate_mean('Pomorskie', 2018)[0][0]*100)
    assert val == '77.40'

def test_contoller_best(ctl):
    results = ctl.find_best_territory()
    assert results[1][1] == 'Małopolskie'

def test_controller_yearly(ctl):
    results = ctl.calculate_yearly_pass_rate('Pomorskie')
    for p, q in zip(results, v_yearly):
        assert '{:d} {:.2f}%'.format(p[0], p[1]*100) == q

def test_controller_compare(ctl):
    results = ctl.compare_two_territories('Pomorskie', 'Podlaskie')
    for p, q in zip(results, v_compare):
        assert '{:d} {:19} {:.2f}%'.format(p[0], p[1], p[2]*100)
