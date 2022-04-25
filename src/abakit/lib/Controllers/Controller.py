from abakit.lib.sql_setup import session, pooledsession

class Controller(object):
    def __init__(self):
        """ setup the attributes for a sql session
        """
        self.session = session
    
    def update_row(self, row):
        try:
            self.session.merge(row)
            self.session.commit()
        except Exception as e:
            print(f'No merge for  {e}')
            self.session.rollback()
    
    def add_row(self,data):
        try:
            self.session.add(data)
            self.session.commit()
        except Exception as e:
            print(f'No merge {e}')
            self.session.rollback()
        finally:
            self.session.close()
    
    def get_row(self,search_dictionary,model):
        query_start = self.session.query(model)
        for key, value in search_dictionary.items():
            query_start = eval(f'query_start.filter(LayerData.{key}=="{value}")')
        return query_start.one()
    
    def row_exists(self,search_dictionary,model):
        return self.get_row(search_dictionary,model) == True
    
    def query_table(self,search_dictionary,model):
        query_start = self.session.query(model)
        for key, value in search_dictionary.items():
            query_start = eval(f'query_start.filter(LayerData.{key}=="{value}")')
        return query_start.all()