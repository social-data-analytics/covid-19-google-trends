labels = {
	# "/g/11j631mnxz": "Molnupiravir\n",
	# "/g/11q8h3trz5": "PF-07321332\n",
    "/g/11qm6vy88k": "Long COVID \n(Condition)",

    '/m/0m7pl': "Anosmia \n(Condition)",
    # '/m/05sfr2': "Ageusia \n(Topic)",
    '/m/05sfr2': "Ageusia",
    '/m/0ddwt': "Insomnia \n(Disorder)",


    '/m/0j5fv': "Headache \n(Condition)",
	"/m/02np4v": "Chest pain\n",
	"/m/013677": "Myalgia\n",
    # '/m/06gx48m': "Chest Tightness \n(Topic)",
    '/m/06gx48m': "Chest Tightness",


	"/m/01j6t0": "Fatigue",
    # "/m/079p0q": "Lightheadedness \n(Topic)",
    "/m/079p0q": "Lightheadedness",
    # '/m/0dl9s3k': "Hip pain \n(Topic)",
    '/m/0dl9s3k': "Hip pain",
    # '/g/11bytn80mf': "Aching Muscle Pain \n(Topic)",
    '/g/11bytn80mf': "Aching Muscle Pain",


    # '/m/029ggh': "Palpitations \n(Topic)",
    '/m/029ggh': "Palpitations",
    '/m/01cdt5': "Shortness of breath \n(Disease)",
    '/m/033mg5': "Dizziness \n(Disorder)",


	"/m/0k_9": "Anxiety \n(Disorder)",
	# "/m/03x69g": "Mental health \n(Topic)",
    "/m/03x69g": "Mental health",
    '/m/02bft': "Major \ndepressive \ndisorder \n(Mental disorder)",
    '/m/0cnmb': "Sleep disorder \n(Medical disorder)",

	"/m/04c_jpd": "Hypochondriasis \n(Condition)",
    "/m/02656gy": "Clouding of \nconsciousness",
	"/m/03l19k": "Ritonavir\n",
}

new_labels = {
	# "/g/11j631mnxz": "Molnupiravir\n",
	# "/g/11q8h3trz5": "PF-07321332\n",
    "/g/11qm6vy88k": "Long COVID",

    '/m/0m7pl': "Anosmia",
    # '/m/05sfr2': "Ageusia \n(Topic)",
    '/m/05sfr2': "Ageusia",
    '/m/0ddwt': "Insomnia",


    '/m/0j5fv': "Headache",
	"/m/02np4v": "Chest pain",
	"/m/013677": "Myalgia",
    # '/m/06gx48m': "Chest Tightness \n(Topic)",
    '/m/06gx48m': "Chest Tightness",


	"/m/01j6t0": "Fatigue",
    # "/m/079p0q": "Lightheadedness \n(Topic)",
    "/m/079p0q": "Lightheadedness",
    # '/m/0dl9s3k': "Hip pain \n(Topic)",
    '/m/0dl9s3k': "Hip pain",
    # '/g/11bytn80mf': "Aching Muscle Pain \n(Topic)",
    '/g/11bytn80mf': "Aching Muscle Pain",


    # '/m/029ggh': "Palpitations \n(Topic)",
    '/m/029ggh': "Palpitations",
    '/m/01cdt5': "Shortness of breath",
    '/m/033mg5': "Dizziness",


	"/m/0k_9": "Anxiety",
	# "/m/03x69g": "Mental health \n(Topic)",
    "/m/03x69g": "Mental health",
    '/m/02bft': "Major depressive disorder",
    '/m/0cnmb': "Sleep disorder",

	"/m/04c_jpd": "Hypochondriasis",
    "/m/02656gy": "Clouding of consciousness",
	"/m/03l19k": "Ritonavir",
}

# print("\n".join([ label.replace("\n", "") for label in labels.values() ]))

tag_to_cluters = {
    "/g/11qm6vy88k": 1,
    "/m/03x69g": 1,
    "/m/03l19k": 1,
    "/m/02656gy": 1,
    '/g/11bytn80mf': 1,

    "/m/01j6t0": 2,
    '/m/02bft': 2,
    '/m/01cdt5': 2,
    '/m/0cnmb': 2,
    '/m/0m7pl': 2,
    '/m/05sfr2': 2,
    "/m/04c_jpd": 2,

    '/m/029ggh': 3,
    '/m/0dl9s3k': 3,
    '/m/06gx48m': 3,

    "/m/013677": 4,
    '/m/0j5fv': 4,
    '/m/033mg5': 4,

    "/m/0k_9": 0,
    "/m/02np4v": 0,
    "/m/079p0q": 0,
    '/m/0ddwt': 0
}

tag_to_colors = {
    "/g/11qm6vy88k": "C1",
    "/m/03x69g": "C1",
    "/m/03l19k": "C1",
    "/m/02656gy": "C1",
    '/g/11bytn80mf': "C1",

    "/m/01j6t0": "C2",
    '/m/02bft': "C2",
    '/m/01cdt5': "C2",
    '/m/0cnmb': "C2",
    '/m/0m7pl': "C2",
    '/m/05sfr2': "C2",
    "/m/04c_jpd": "C2",

    '/m/029ggh': "C3",
    '/m/0dl9s3k': "C3",
    '/m/06gx48m': "C3",

    "/m/013677": "C4",
    '/m/0j5fv': "C4",
    '/m/033mg5': "C4",

    "/m/0k_9": "C5",
    "/m/02np4v": "C5",
    "/m/079p0q": "C5",
    '/m/0ddwt': "C5"
}

