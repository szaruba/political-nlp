import tkinter as tk
import random
import numpy as np
import re

class Labeler:
    IDX_UNLABELED_ID                = 0
    IDX_UNLABELED_SPEECH            = 6
    IDX_UNLABELED_PRE_CONTEXT       = 7
    IDX_UNLABELED_POST_CONTEXT      = 8
    IDX_UNLABELED_CATEGORIES_START  = 9
    CATEGORY_NAMES                  = ['MASKS', 'LOCKDOWN', 'VACCINES', 'TESTING', 'DISTANCING']
    IDX_LABELED_ID                  = 2

    # only these will get loaded
    DESIRED_CATEGORIES = ['LOCKDOWN']

    KEYWORDS_REGEX = 'mask|ffp2|mund.?nasen|[lL]ock.?[dD]own|impf|pcr|testet|testung|tests|testen|distanc|abstand|social.d'

    unlabeled_samples = []
    unlabeled_dataset_path = '../protocols/secondary_format/massnahmen.csv'
    labeled_dataset_path = '../protocols/labelled/massnahmen.csv'
    count_total = 0
    displayed_sample = None
    context_displayed = False

    def __init__(self):
        window = tk.Tk()

        self.l_progress = tk.Label()
        self.l_progress.pack()

        self.l_cat = tk.Label(text="Categories: ")
        self.l_cat.pack()

        self.t_precontext = tk.Text(height=10)
        self.t_sentence = tk.Text(height=10)
        self.t_postcontext = tk.Text(height=10)

        self.t_precontext.pack()
        self.t_sentence.pack()
        self.t_postcontext.pack()

        b_con = tk.Button(text="Contra (-)")
        b_neut = tk.Button(text="Neutral (o)")
        b_pro = tk.Button(text="Pro (+)")
        b_irr = tk.Button(text="Irrelevant (x)")

        b_con.pack()
        b_neut.pack()
        b_pro.pack()
        b_irr.pack()

        # Bind events
        window.bind("<Left>", self.handle_contra)
        window.bind("<Down>", self.handle_neutral)
        window.bind("<Right>", self.handle_pro)
        window.bind("<Up>", self.handle_irrelevant)
        b_con.bind("<Button-1>", self.handle_contra)
        b_neut.bind("<Button-1>", self.handle_neutral)
        b_pro.bind("<Button-1>", self.handle_pro)
        b_irr.bind("<Button-1>", self.handle_irrelevant)

        self.load_samples()
        self.load_unlabeled_sample()

        window.mainloop()

    def load_samples(self):
        """Loads all remaining unlabeled samples"""
        with open(self.labeled_dataset_path, 'r') as f:
            labeled_ids = [line.split('\t')[self.IDX_LABELED_ID] for line in f]
        with open(self.unlabeled_dataset_path, 'r') as f:
            all_lines = [line.replace('\n', '') for line in f.readlines()]
            # filter BY DESIRED_CATEGORIES
            all_lines = [sample for sample in all_lines if self.sample_has_category(sample, self.DESIRED_CATEGORIES)]
            self.count_total = len(all_lines)
            self.unlabeled_samples = [line for line in all_lines if line.split('@@')[self.IDX_UNLABELED_ID] not in labeled_ids]

        self.update_progress()

    def sample_has_category(self, sample, desired_categories):
        sample_cols = sample.split('@@')
        category_flags = sample_cols[self.IDX_UNLABELED_CATEGORIES_START:
                                     self.IDX_UNLABELED_CATEGORIES_START + len(self.CATEGORY_NAMES)]
        category_flags = [item == 'True' for item in category_flags]
        sample_categories = np.array(self.CATEGORY_NAMES)[category_flags]
        return bool(set(sample_categories) & set(desired_categories))

    def load_unlabeled_sample(self):
        """Clears previous sample and loads the next random unlabeled sample for labeling"""
        self.context_displayed = False
        self.set_textbox_text(self.t_precontext, '')
        self.set_textbox_text(self.t_postcontext, '')
        if len(self.unlabeled_samples) == 0:
            self.set_textbox_text(self.t_sentence, "Congratulations! All samples are processed, take a well-deserved break. ")
            return
        rand_idx = random.randrange(0, len(self.unlabeled_samples))
        self.displayed_sample = self.unlabeled_samples[rand_idx]
        sample_cols = self.displayed_sample.split('@@')
        speech = sample_cols[self.IDX_UNLABELED_SPEECH]
        category_flags = sample_cols[self.IDX_UNLABELED_CATEGORIES_START:
                                     self.IDX_UNLABELED_CATEGORIES_START + len(self.CATEGORY_NAMES)]
        category_flags = [item == 'True' for item in category_flags]
        self.set_textbox_text(self.t_sentence, speech)
        self.l_cat.config(text=', '.join(np.array(self.CATEGORY_NAMES)[category_flags]))

    def load_context(self):
        sample_cols = self.displayed_sample.split('@@')
        pre_context = sample_cols[self.IDX_UNLABELED_PRE_CONTEXT]
        post_context = sample_cols[self.IDX_UNLABELED_POST_CONTEXT]
        self.set_textbox_text(self.t_precontext, pre_context)
        self.set_textbox_text(self.t_postcontext, post_context)
        self.context_displayed = True

    def update_progress(self):
        count_labeled = self.count_total - len(self.unlabeled_samples)
        self.l_progress.config(text=f'{count_labeled}/{self.count_total} remaining: {len(self.unlabeled_samples)} '
                                    f'({"{:.2f}".format(len(self.unlabeled_samples) / self.count_total * 100)}%)')

    def set_textbox_text(self, textbox, text):
        textbox.tag_delete(textbox.tag_names())
        textbox.delete('1.0', tk.END)
        textbox.insert('1.0', text)
        self.highlight_keywords(textbox)

    def highlight_keywords(self, textbox):
        text = textbox.get("1.0", tk.END)
        pattern = re.compile(self.KEYWORDS_REGEX, re.I)
        result = pattern.search(text, 0)
        while result:
            match_end_idx = result.endpos
            for match in result.regs:
                match_end_idx = match[1]
                textbox.tag_add('highlight', f'1.{match[0]}', f'1.{match_end_idx}')
            textbox.tag_config('highlight', background='black', foreground='white')
            result = pattern.search(text, match_end_idx)

    def label_displayed_sample(self, label):
        with open(self.labeled_dataset_path, 'a+') as f:
            sample_cols = self.displayed_sample.split('@@')

            # merge context if used
            if self.context_displayed:
                sample_cols[self.IDX_UNLABELED_SPEECH] = sample_cols[self.IDX_UNLABELED_PRE_CONTEXT] + ' ' + \
                                                         sample_cols[self.IDX_UNLABELED_SPEECH] + ' ' + \
                                                         sample_cols[self.IDX_UNLABELED_POST_CONTEXT]
            cat_start_idx = self.IDX_UNLABELED_CATEGORIES_START
            cat_end_idx = self.IDX_UNLABELED_CATEGORIES_START + len(self.CATEGORY_NAMES)
            out_cols = sample_cols[0:self.IDX_UNLABELED_SPEECH+1] + sample_cols[cat_start_idx:cat_end_idx]
            out_cols.insert(0, str(self.context_displayed))
            out_cols.insert(0, label)
            line = '\t'.join(out_cols) + '\n'
            f.write(line)
            f.flush()

            self.unlabeled_samples.remove(self.displayed_sample)
            self.update_progress()

    def handle_contra(self, event):
        print("contra")
        self.label_displayed_sample('-')
        self.load_unlabeled_sample()

    def handle_neutral(self, event):
        print("neutral")
        if self.context_displayed:
            self.label_displayed_sample('o')
            self.load_unlabeled_sample()
        else:
            self.load_context()

    def handle_pro(self, event):
        print("pro")
        self.label_displayed_sample('+')
        self.load_unlabeled_sample()

    def handle_irrelevant(self, event):
        print("irrelevant")
        self.label_displayed_sample('x')
        self.load_unlabeled_sample()


if __name__ == '__main__':
    Labeler()