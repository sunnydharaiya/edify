from django.shortcuts import render, get_object_or_404
from .models import GenericActivity, IdentifyPicture, Category, ImageMatchingActivity, ImageWordPair, MissingWord, PrefixSuffixActivity, PrefixSuffixWord, PrefixSuffixOption, SynonymAntonymActivity, WordPair, UnscrambleActivity, UnscrambleEntry
from django.http import Http404
from django.db.models import Prefetch
from random import shuffle

def generic_activity_detail(request, category_slug, activity_slug):
    category = get_object_or_404(Category, slug=category_slug)
    activity = get_object_or_404(GenericActivity, title__iexact=activity_slug.replace('-', ' '), category=category)
    
    # Check for IdentifyPicture
    pictures = IdentifyPicture.objects.filter(activity=activity)
    if pictures.exists():
        return render(request, 'vocabulary/identify_picture.html', {
            'activity': activity,
            'category': category,
            'pictures': pictures
        })
    
    # Check for ImageMatchingActivity
    image_matching_activity = ImageMatchingActivity.objects.filter(activity=activity).first()
    if image_matching_activity:
        image_word_pairs = ImageWordPair.objects.filter(image_matching_activity=image_matching_activity)
        if image_word_pairs.exists():
            return render(request, 'vocabulary/image_matching_activity_detail.html', {
                'activity': activity,
                'category': category,
                'image_matching_activity': image_matching_activity,
                'image_word_pairs': image_word_pairs
            })
    
    # Check for MissingWord
    missing_words = MissingWord.objects.filter(activity=activity)
    if missing_words.exists():
        return render(request, 'vocabulary/missing_word_activity_detail.html', {
            'activity': activity,
            'category': category,
            'missing_words': missing_words
        })
    

    prefix_suffix_activities = PrefixSuffixActivity.objects.filter(activity=activity).prefetch_related(
        Prefetch('words', queryset=PrefixSuffixWord.objects.prefetch_related('options'))
    )

    # Inject correct option ID into each word
    for activity in prefix_suffix_activities:
        for word in activity.words.all():
            correct_option = next((opt for opt in word.options.all() if opt.is_answer), None)
            word.correct_option_id = correct_option.id if correct_option else None

    if prefix_suffix_activities.exists():
        return render(request, 'vocabulary/prefix_suffix_activity_detail.html', {
            'activity': activity,
            'category': category,
            'prefix_suffix_activities': prefix_suffix_activities,
        })

    synonym_antonym_activities = SynonymAntonymActivity.objects.filter(activity=activity).prefetch_related(
        Prefetch('word_pairs') 
    )
    if synonym_antonym_activities.exists():
        return render(request, 'vocabulary/synonym_antonym_activity_detail.html', {
            'activity': activity,
            'category': category,
            'synonym_antonym_activities': synonym_antonym_activities,
        })
    if activity_slug == 'wordsearch':
        if category_slug == 'grade-2':
            title = "NAMES OF CLOTHES"
            wordsearch_data = [
                ['t,1','s,1','e,1','v,1','c','t,1','r','o','f','v','u','n,1','b','x','v'],
                ['u','n ','j','i,1','e,1','b','z','m','i','f','g','a,1','z','m','a'],
                ['d','m','r','k,1','d,1','j','z','r','u','c','h','g,1','g','u','f'],
                ['q','c','c,1','s','l','o,1','c','b','o','n','o','i,1','h','u','p'],
                ['u','a,1','e','r','c','k','o,1','n','u','z','w','d,1','d','o','c'],
                ['j,1','k','a','s','u','l','p','h,1','s,1','c,1','a,1','r,1','f,1','w','u'],
                ['d','q','o','p','i','m','n','g','d','v','l','a,1','h','g','p'],
                ['t','r','k','t','r,1','e,1','t,1','a,1','e,1','w,1','s,1','c,1','g,1','c','q'],
                ['o','j,1','v','g','s','h','o','v','v','k,1','g','z','o,1','y','x'],
                ['k','r','e,1','a','b','u','j','g','i,1','y','j','p','w,1','d','v'],
                ['a','i','v','a,1','o','u','m','r,1','y','a','c','i','n,1','b','z'],
                ['w','t','y','c','n,1','r','t,1','v','k','z','i','y','g','q','z'],
                ['d','p','w','x','f','s,1','t','i','j','h','x','e','j','n','k'],
                ['p','l','u','q','k','s','c','w','k','w','g','s','w','i','o'],
                ['t','k','a','p','u','b','c','r','s','z','s','f','r','v','f'],
            ]
            btn_text = [
                ['sweater'],
                ['hoodie'],
                ['cardigan'],
                ['jacket'],
                ['scarf'],
                ['jeans'],
                ['gown'],
                ['skirt'],
                ['vest'],
                ['Tie'],
            ]
        elif category_slug == 'grade-3':
            title = "Construction Vehicles"
            wordsearch_data = [
                ['R,4','n','o','q','w','h','n','u','y','n','e,9','t','o','t','q'],
                ['B','o,4','t','e','j','r','d','k','g','r','x,9','n','m','j','o'],
                ['G','a','a,4','d,1','u,1','m,1','p,1','t,3','r,1','u,1','c,9','k,1','a','f','r'],
                ['K','g','y','d,4','r,1','y','r,3','y','b','k','a,9','j','d','r','d'],
                ['b,5,1','o','x','e,1','r,4','a,3','i','k','x','c','v,9','y','k','a','c'],
                ['D','a,5','x,1','d','c,3','o,4','i','h','u','o','a,9','t,4','r','d','a'],
                ['W','i,1','c,5','t,3','y','c','l,4','i','m','o','t,9','n,4','y','z','e'],
                ['M,1','d','o,3','k,5','d','o','z','l,4','k','j','o,9','e,4','m','i','a'],
                ['F','r,3','b','o','h,5','f','n','f','e,4','k','r,9','m,4','k','m','w'],
                ['B,2','u,2','l,2','l,2','d,2','o,2','z,2','e,2','r,2','r,4','i','e,4','l','g','h'],
                ['F','q','d','p','p','x','e,5','t','w','x','g','c,4','t','t','n'],
                ['T,7','f,7','i,7','l,7','k,7','r,7','o,7','f,7','a','y','q','a','w','c','h'],
                ['Z','a','n','y','m','d','g','d','l','d','t','g','g','r','f'],
                ['Y','t','z','f','w','b','r','u','h','c','i','b','p','z','q'],
                ['n','f','o','y','z','y','j','c','z','p','m','k','f','o','e'],
            ]
            btn_text = [
                ['dumptruck'],
                ['Bulldozer'],
                ['tractor'],
                ['cement'],
                ['backhoe'],
                ['mixer'],
                ['roadroller'],
                ['forklift'],
            ]
        elif category_slug == 'grade-4':
            title = "names of musical instrument"
            wordsearch_data = [
                ['N','e','c','t','t','t','e','n','r','i','t','t','e','m'],
                ['X','e,1','t,1','u,1','l,1','f,1','s','o','i','t,1','u,1','b,1','a,1','j'],
                ['O','n','g,1','u,1','i,1','t,1','a,1','r,1','r','m','r','r','a','t'],
                ['n','a','s','p','i','i','d','s','n','i','h','t','t','a'],
                ['B','r','s,1','a,1','x,1','o,1','p,1','h,1','o,1','n,1','e,1','a','a','h'],
                ['t,1','h,1','v','a','d','t,1','r,1','u,1','m,1','p,1','e,1','t,1','x','n'],
                ['A,1','a,1','e','a','b,1','p','a','t','o','a','m','r','b','h'],
                ['m,1','r,1','i','o','x','a,1','m','u','t','x','a','m','r','a'],
                ['B,1','m,1','n','i','r','p','n,1','a','t','g','a','i','u','i'],
                ['O,1','o,1','d,1','r,1','u,1','m,1','s,1','j,1','t','a','m','p,1','n','a'],
                ['r,1','n,1','n','i','r','o','i','p','o,1','u','u','i,1','n','t'],
                ['I,1','i,1','p','u','o','i','h,1','a,1','r,1','p,1','a,1','a,1','o','b'],
                ['N,1','c,1','a','v,1','i,1','o,1','l,1','i,1','n,1','f','o','n,1','a','e'],
                ['e,1','a,1','m','i','j','n','a','n','v','i','s','o,1','g','o'],
            ]
            btn_text = [
                ['trumpet'],
                ['harmonica'],
                ['drums'],
                ['piano'],
                ['saxophone'],
                ['tambourine'],
                ['guitar'],
                ['violin'],
                ['banjo'],
                ['flute'],
                ['tuba'],
                ['harp'],
            ]
        elif category_slug == 'grade-5':
            title = "Museum"
            wordsearch_data = [
                ['A,1','a,1','u','c','c','r','r','e','h','e','n','g','n','n'],
                ['R,1','r,1','r','h','i','m,1','i','a','c','a','u','h','n','t'],
                ['C,1','c,1','e,1','u','a','o,1','u','l','e','i','e','r','r','b'],
                ['H,1','h,1','x,1','e','n','n,1','r','n','i','s,1','e','a','l','t'],
                ['I,1','e,1','h,1','n','i,1','u,1','y','r,1','l','c,1','i','i','a,1','t'],
                ['T,1','o,1','i,1','c','n,1','m,1','c','e,1','y,1','u,1','e','r','r,1','r'],
                ['E,1','l,1','b,1','e','v,1','e,1','r','c,1','r,1','l,1','r','v','c,1','r'],
                ['C,1','o,1','i,1','c,1','e,1','n,1','o','o,1','e,1','p,1','n','e','h,1','r'],
                ['T,1','g,1','t,1','u,1','n,1','t,1','n','r,1','l,1','t,1','a','e','i,1','t'],
                ['U,1','y,1','i,1','r,1','t,1','u','i','d,1','l,1','u,1','r','r','v,1','g'],
                ['R,1','d','o,1','a,1','i,1','n','o','l','a,1','r,1','r','u','e,1','i'],
                ['E,1','i','n,1','t,1','o,1','t','g','e','g,1','e,1','x','y','o','c'],
                ['O','r','h','o,1','n,1','t','e','t','h','i','a','u','o','h'],
                ['i','t','t','r,1','n','i','e','u','r','t','y','n','o','e'],
            ]
            btn_text = [
                ['Exibition'],
                ['sculpture'],
                ['archeology'],
                ['record'],
                ['architecture'],
                ['archive'],
                ['invention'],
                ['gallery'],
                ['monument'],
                ['curator'],
            ]
        return render(request, 'vocabulary/wordsearch_activity_detail.html', {
            'activity': activity,
            'category': category,
            'wordsearch_data': wordsearch_data,
            'btn_text': btn_text,
            'title': title,
        })

    if activity_slug == 'crossword':
        if category_slug == 'grade-2':
            title = "NAMES OF SPORTS"
            crossword_data = [
                ['', '', '', '', '', '', '', '', ['T', '1'], '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', ['S', '2'], '', '', '', ['R', ''], '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', ['N', ''], '', '', '', ['I', ''], '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', ['O', ''], '', '', ['K', '3'], ['A', ''], ['Y', ''], ['A', ''], ['K', ''], ['I', ''], ['N', ''], ['G', ''], '', '', ''],
                ['', ['J', '4'], ['U', ''], ['D', ''], ['O', ''], '', '', '', ['T', ''], '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', ['K', ''], '', '', '', ['H', ''], '', '', '', '', '', '', '', '', ''],
                [['V', '5'], ['O', ''], ['L', ''], ['L', ''], ['E', ''], ['Y', ''], ['B', '6'], ['A', ''], ['L', ''], ['L', ''], '', '', '', '', '', '', '', ''],
                ['', '', '', '', ['R', ''], '', ['A', ''], '', ['O', ''], '', '', '', '', '', ['G', '7'], ['O', ''], ['L', ''], ['F', '']],
                ['', '', '', '', '', '', ['S', ''], '', ['N', ''], '', '', '', '', '', ['Y', ''], '', '', ''],
                ['', '', '', '', '', '', ['K', ''], '', '', '', '', '', '', '', ['M', ''], '', '', ''],
                ['', '', '', '', '', '', ['E', ''], '', ['S', '8'], ['W', ''], ['I', ''], ['M', ''], ['M', ''], ['I', ''], ['N', ''], ['G', ''], '', ''],
                ['', '', '', '', '', '', ['T', ''], '', '', '', '', '', '', '', ['A', ''], '', '', ''],
                ['', '', '', '', '', '', ['B', ''], '', '', '', '', '', '', '', ['S', ''], '', '', ''],
                ['', '', '', '', '', '', ['A', ''], '', '', '', '', '', '', '', ['T', ''], '', '', ''],
                ['', '', '', '', '', '', ['L', '9'], ['A', ''], ['W', ''], ['N', ''], ['T', ''], ['E', ''], ['N', ''], ['N', ''], ['I', ''], ['S', ''], '', ''],
                ['', '', '', '', '', '', ['L', ''], '', '', '', '', '', '', '', ['C', ''], '', '', ''],
            ]
            across = [
                ['3. kayaking'],
                ['4. judo'],
                ['5. volleyball'],
                ['7. golf'],
                ['8. swimming'],
                ['9. lawntennis'],
            ]
            down = [
                ['1. triathlon'],
                ['2. snooker'],
                ['6. basketball'],
                ['7. gymnastic'],
            ]
        elif category_slug == 'grade-3':
            title = "Occupation and Jobs"
            crossword_data = [
                ['', '', '', '', '', '', '', ['S', '1'], ['A', ''], ['I', ''], ['L', ''], ['O', ''], ['R', ''], '', ''],
                ['', '', '', '', '', '', '', ['O', ''],'', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', ['L', ''],'', '', '', '', '', '', '', ''],
                ['', '', '', '', '', ['M', '2'], '', ['D', ''],'', '', '', '', '', '', '', ''],
                ['', '', '', '', '', ['E', ''], '', ['I', ''],'', '', ['L', '3'], '', '', '', '', ''],
                ['', '', '', '', ['S', '4'], ['C', ''], ['I', ''], ['E', ''],['N', ''], ['T', ''], ['I', ''], ['S', ''], ['T', ''], '', '', ''],
                ['', '', '', '', '', ['H', ''], '', ['R', ''],'', '', ['B', ''], '', '', '', '', ''],
                ['', ['T', '5'], '', '', '', ['A', ''], '', '','',  '',['R', ''], '', '', '', '', ''],
                ['', ['E', ''], '', '', '', ['N', ''], '', '','',  '', ['A', ''],'', '', ['A', '6'], '', ''],
                [['M', '7'], ['A', ''], ['G', ''], ['I', ''], ['C', ''], ['I', ''], ['A', ''], ['N', ''],'', '', ['R', ''], '', '', ['R', ''], '', ''],
                ['', ['C', ''], '', '', '', ['C', ''], '', '','', '', ['I', ''], '', '', ['T', ''], '', ''],
                [['C', '8'], ['H', ''], ['E', ''], ['F', ''], '', '', '', '','', '', ['A', ''], '', '', ['I', ''], '', ''],
                ['', ['E', ''], '', '', '', '', '', '',['D', '9'], ['E', ''], ['N', ''], ['T', ''], ['I', ''], ['S', ''], ['T', ''], ''],
                ['', ['R', ''], '', '', '', '', '', '','', '', '', '', '', ['T', ''], '', ''],
            ]
            across = [
                ['1. Some who can sails boat and ship. '],
                ['4. New is possible, due to inventions made by them. '],
                ['7. A person with the talent of creating magic. '],
                ['8. He cooks delicious meal. '],
                ['9. A person who treats our gums and teeth.'],
            ]
            down = [
                ['1. People who safe guard our country. '],
                ['2. A broken car is repaired by'],
                ['3. He/she in charge of books, magazines. '],
                ['5. The second mother of the child. '],
                ['6. A creative person with talent to draw and paint.'],
            ]
        elif category_slug == 'grade-4':
            title = "Space Vocabulary"
            crossword_data = [
                ['', '', '', '', '', '', '', '', '', '', '',['A', 1], ['S', ''], ['T', 2], ['E', ''], ['R', ''], ['O', ''], ['I', ''], ['D', ''], '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', '', '', ['E', ''], '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', '', ['P', '3'], ['L', ''], ['A', ''], ['N', ''], ['E', ''], ['T', ''], '', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', ['E', '4'], '', ['E', ''], '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', ['A', ''], '', ['S', ''], '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', ['R', ''], '', ['C', ''], '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', '', '', '', '', ['T', ''], '', ['O', '5'], ['R', ''], ['B', ''], ['I', ''], ['T', ''], '', '', ''],
                ['', '', '', '', '', ['S', '6'], ['P', ''], ['A', '7'], ['C', ''], ['E', ''], ['S', ''], ['H', ''], ['I', ''], ['P', ''], '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '',['S', '4'], '', '', '', '',  '', ['E', ''], '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '',['T', ''], '', '', '', '',  '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', ['A', '8'], ['S', ''], ['T', ''],['R', ''], ['O', ''], ['N', ''], ['O', ''],['M', ''], ['Y', ''], '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '',['O', ''], '', '', '', '',  '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '',['N', ''], '', '', '', '',  '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', ['G', '9'],['A', ''], ['L', ''], ['A', ''], ['X', ''], ['Y', ''],  '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '',['U', ''], '', '', '', '',  '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', ['S', '10'],['A', ''],['T', ''], ['E', ''], ['L', ''], ['L', ''], ['I', ''],  ['T', ''], ['E', ''], '', '', '', '', '', '', ''],
            ]
            across = [
                ['1. a small rocky object that moves around the sun'],
                ['3. any large bodies that revolve around the sun'],
                ['5. the curved path of a celestial object or spacecraft round a star,planet or moon'],
                ['6. a vehicle used for travelling in space'],
                ['8. study of everything in universe'],
                ['9. a system of millions or billions of stars, together with gas and dust'],
                ['10. an object sent to space inorder to collect information of space'],
            ]
            down = [        
                ['2. an object used to see distant objects in space'],
                ['4. the planet on which we live'],
                ['7. a person who travels into spacecraft'],
            ]
        elif category_slug == 'grade-5':
            title = "Achievement"
            crossword_data = [
                ['', '', '', '', '', '', '',  '', '', '', '', '', '',['F', '1','1'], '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '',  '', '', '', '', '', ['G', '2','1'],['L', '','1'], ['O', ''], ['R', ''], ['Y', ''], '', '', '', ''],
                ['', '', '', '', '', '', '',  '', '', '', '', '', '',['O', ''], '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '',  '', '', '', '', '', '',['U', ''], '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', ['A', '3','1'], ['C', '4','1'], ['H', ''], ['I', ''], ['E', ''], ['V', ''], ['E', ''], ['R', '','1'], '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', ['O', ''], '', '', '', '', '', ['I', ''], '', '', '', '', '', '', ''],
                ['', '', '', ['A', '5','1'], ['D', ''], ['V', ''], ['A', ''], ['N', '','1'], ['C', ''], ['E', ''], '','',  ['A', '6','1'], ['S', '','1'], ['P', ''], ['I', ''], ['R', ''], ['E', '']],
                ['', '', '', '', '', '', '', ['G', ''], '', '', '', '', '', ['H',''],'', '', '', '', '', '', ''],
                [['B', '7','1'], ['R', ''], ['E', ''], ['A', ''], ['K', ''], ['T', ''], ['H', ''], ['R', '','1'], ['O', ''], ['U', ''], ['G', ''], ['H', '','1'], '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', ['A', ''], '', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', ['T', '8','1'], ['R', ''], ['I', ''], ['U', ''], ['M', ''], ['P', ''], ['H', '','1'], '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', ['U', ''], '', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', ['L', ''], '', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', ['A', '9','1'], ['C', ''], ['C', ''], ['O', ''], ['M', ''], ['P', ''], ['L', ''], ['I', ''], ['S', ''], ['H', '','1'], '', '', '', ''],
                ['', '', '', '', '', '', '', ['T', ''], '', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['', '', '', '', ['C', '10','1'], ['O', ''], ['M', ''], ['E', '','1'], ['B', ''], ['A', ''], ['C', ''], ['K', '','1'], '', '', '', '', '', '', '', '', ''],
            ]
            across = [
                ['2. high renown or honour won by notable achievemnents.'],
                ['3. a person who achicves a high or specified level of success'],
                ['5. to move forward in a purposeful way.'],
                ['6. to direct one hopes or ambitions towards achieving something.'],
                ['7. an important discovery or event that helps to improve a situation or provide an answer to a problenm '],
                ['8. a great victory or achievement. 9. to achieve or comnplete successfully. '],
                ['10. to retun to the activity in which the person have formerly been successful.'],
            ]
            down = [
                ['1. grow or develop in a healthy or vigorous way. especially as the result of a particularly congenial environment.'],
                ['4. give (someone) one good wishes when something special or pleasant has happened to them'],
            ]
        return render(request, 'vocabulary/crossword_activity_detail.html', {
            'activity': activity,
            'category': category,
            'crossword_data': crossword_data,
            'across': across,
            'down': down,
            'title': title,
        })

    unscramble_activities = UnscrambleActivity.objects.filter(activity=activity).prefetch_related('entries')
    for act in unscramble_activities:
        for entry in act.entries.all():
            words = entry.text.strip().split()
            shuffled = words[:]
            shuffle(shuffled)
            entry.original_words = words
            entry.shuffled_words = shuffled

    return render(request, 'vocabulary/unscramble_activity_detail.html', {
        'activity': activity,
        'category': category,
        'unscramble_activities': unscramble_activities,
    })

    

    raise Http404("No activities found for this category and slug")


