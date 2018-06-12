class Article:

    def __init__(self, args):
        self.title = args[0]

        try:
            self.ids = set(args[1])
        except Exception:
            print(args[1])
            self.ids = [set(x) for x in args[1] if x is not None]

        if args[2] is not None:
            self.ref_list = [set(x) for x in args[2] if x is not None]
        else:
            self.ref_list = []

        self.uniq_id = None

    def __eq__(self, other):
        if isinstance(other, Article):
            return self.compare(other)

        return False

    def compare(self, article):
        if len(self.ids.intersection(article.ids)) != 0:
            return True

        if self.normalize_title() == article.normalize_title():
            return True

        return False

    def set_id(self, id):
        self.uniq_id = id
        return self

    def normalize_title(self):
        return self.title.lower().replace(' ', '')

    def __hash__(self):
        hsh = hash(self.title)
        for id in self.ids:
            hsh = hsh ^ hash(id)
        return hsh






