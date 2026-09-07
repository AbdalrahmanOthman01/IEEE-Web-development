
const ayat = [
    "﴿إِنَّ هَـذَا الْقُرْآنَ يِهْدِي لِلَّتِي هِيَ أَقْوَمُ وَيُبَشِّرُ الْمُؤْمِنِينَ الَّذِينَ يَعْمَلُونَ الصَّالِحَاتِ أَنَّ لَهُمْ أَجْراً كَبِيراً﴾",

    "﴿اللَّهُ نَزَّلَ أَحْسَنَ الْحَدِيثِ كِتَاباً مُّتَشَابِهاً مَّثَانِيَ تَقْشَعِرُّ مِنْهُ جُلُودُ الَّذِينَ يَخْشَوْنَ رَبَّهُمْ ثُمَّ تَلِينُ جُلُودُهُمْ وَقُلُوبُهُمْ إِلَى ذِكْرِ اللَّهِ ذَلِكَ هُدَى اللَّهِ يَهْدِي بِهِ مَنْ يَشَاءُ وَمَن يُضْلِلِ اللَّهُ فَمَا لَهُ مِنْ هَادٍ﴾",

    "﴿إِنَّ الَّذِينَ يَتْلُونَ كِتَابَ اللَّهِ وَأَقَامُوا الصَّلَاةَ وَأَنفَقُوا مِمَّا رَزَقْنَاهُمْ سِرًّا وَعَلَانِيَةً يَرْجُونَ تِجَارَةً لَّن تَبُورَ﴾",

    "﴿وَلَقَدْ يَسَّرْنَا الْقُرْآنَ لِلذِّكْرِ فَهَلْ مِن مُّدَّكِرٍ﴾",

    "﴿وَالَّذِينَ يُمَسِّكُونَ بِالْكِتَابِ وَأَقَامُوا الصَّلَاةَ إِنَّا لَا نُضِيعُ أَجْرَ الْمُصْلِحِينَ﴾",

    "﴿قُلْ لَّوْ كَانَ الْبَحْرُ مِدَادًا لِّكَلِمَاتِ رَبِّي لَنَفِدَ الْبَحْرُ قَبْلَ أَن تَنفَدَ كَلِمَاتُ رَبِّي وَلَوْ جِئْنَا بِمِثْلِهِ مَدَدًا﴾",

    "﴿وَلَوْ أَنَّمَا فِي الْأَرْضِ مِن شَجَرَةٍ أَقْلَامٌ وَالْبَحْرُ يَمُدُّهُ مِن بَعْدِهِ سَبْعَةُ أَبْحُرٍ مَّا نَفِدَتْ كَلِمَاتُ اللَّهِ إِنَّ اللَّهَ عَزِيزٌ حَكِيمٌ﴾"
];


const ahadith = [
    "خيركم من تعلم القرآن وعلمه.",
    "إن الله لا ينظر إلى صوركم ولكن ينظر إلى قلوبكم.",
    "يسروا ولا تعسروا وبشروا ولا تنفروا.",
    "الدال على الخير كفاعله.",
    "تبسمك في وجه أخيك صدقة.",
    "الماهر بالقرآن مع السفرة الكرام البررة.",
    "إنما الأعمال بالنيات، وإنما لكل امرئ ما نوى."
];


const courses = {

    adults: [
        "حلقات البنين",
        "حلقة سورة الأنعام و الأعراف",
        "حلقة جزء عم",
        "حلقة جزء المجادلة",
        "حلقة سورة البقرة",
        "حلقة سورة النساء"
    ],

    kids: [
        "حلقة جزء عم",
        "حلقة جزء تبارك",
        "حلقة جزء المجادلة",
        "حلقة جزء الأحقاف"
    ],

    azhar: [
        "مجموعة الشورى",
        "سورة آل عمران",
        "سورة المائدة",
        "من الفرقان الى القصص",
        "من يس الى فصلت",
        "من الاسراء الى طه"
    ]

};


const announcements = [
    {
        title: "بدء التسجيل",
        body: "تم فتح باب التسجيل للحلقات الجديدة لجميع الفئات."
    },

    {
        title: "حلقات الأونلاين",
        body: "تم فتح مجموعات جديدة على التليجرام لسورة البقرة وآل عمران."
    },

    {
        title: "اختبارات تحديد المستوى",
        body: "تعقد الاختبارات أسبوعياً قبل الالتحاق بالحلقات."
    },

    {
        title: "دورات التجويد",
        body: "بدء دورة التجويد النظري والأكاديمية الميسرة قريبًا."
    }
];


const timetable = [

    {
        day: "الأحد، الثلاثاء، الخميس",
        activity: "سورة الأنعام والأعراف للسيدات",
        time: "10 ص",
        hall: "الشيخ محمد"
    },

    {
        day: "الأحد، الثلاثاء، الخميس",
        activity: "جزء عم للكبار",
        time: "6 م",
        hall: "أ/ إسراء"
    },

    {
        day: "السبت، الاثنين، الأربعاء",
        activity: "جزء المجادلة للكبار",
        time: "4 م",
        hall: "أ/ صباح"
    },

    {
        day: "السبت، الاثنين، الأربعاء",
        activity: "سورة البقرة",
        time: "4 م",
        hall: "أ/ قسمة"
    },

    {
        day: "الأحد، الثلاثاء، الخميس",
        activity: "سورة النساء",
        time: "10 ص",
        hall: "أ/ صباح"
    },

    {
        day: "السبت، الاثنين، الأربعاء",
        activity: "جزء عم للأطفال (1)",
        time: "4 م",
        hall: "أ/ فاطمة قشطة، أ/ فاطمة الجمل"
    },

    {
        day: "السبت، الاثنين، الأربعاء",
        activity: "جزء عم للأطفال (2)",
        time: "6 م",
        hall: "أ/ آية، أ/ عبير"
    },

    {
        day: "الأحد، الثلاثاء، الخميس",
        activity: "جزء عم للأطفال (3)",
        time: "4 م",
        hall: "أ/ آلاء"
    },

    {
        day: "الأحد، الثلاثاء، الخميس",
        activity: "جزء عم للأطفال (4)",
        time: "6 م",
        hall: "أ/ آية"
    },

    {
        day: "السبت، الاثنين، الأربعاء",
        activity: "جزء الأحقاف للأطفال",
        time: "6 م",
        hall: "أ/ أسماء"
    },

    {
        day: "الأحد، الثلاثاء، الخميس",
        activity: "جزء المجادلة للأطفال",
        time: "6 م",
        hall: "أ/ قسمة"
    },

    {
        day: "السبت، الاثنين، الأربعاء",
        activity: "جزء تبارك للأطفال",
        time: "6 م",
        hall: "أ/ قسمة"
    },

    {
        day: "السبت، الاثنين، الأربعاء",
        activity: "مجموعة الشورى (أزهر)",
        time: "10 ص",
        hall: "أ/ عمر"
    },

    {
        day: "السبت، الاثنين، الأربعاء",
        activity: "من يس إلى فصلت (أزهر)",
        time: "10 ص",
        hall: "أ/ صباح"
    },

    {
        day: "السبت، الاثنين، الأربعاء",
        activity: "من الفرقان إلى القصص (أزهر)",
        time: "10 ص",
        hall: "أ/ نورهان"
    },

    {
        day: "السبت، الاثنين، الأربعاء",
        activity: "من الإسراء إلى طه (أزهر)",
        time: "10 ص",
        hall: "أ/ هنا"
    },

    {
        day: "الأحد، الثلاثاء، الخميس",
        activity: "من يونس إلى هود (أزهر)",
        time: "10 ص",
        hall: "أ/ عمر"
    },

    {
        day: "السبت، الاثنين، الأربعاء",
        activity: "سورة المائدة (أزهر)",
        time: "10 ص",
        hall: "أ/ نورهان"
    },

    {
        day: "السبت، الاثنين، الأربعاء",
        activity: "سورة آل عمران (أزهر)",
        time: "10 ص",
        hall: "أ/ هنا"
    }

];



function renderAnnouncements() {

    const latestDiv = document.getElementById("latest");

    if (!latestDiv) {
        return;
    }

    latestDiv.innerHTML = "";

    announcements.forEach(function (announcement) {

        const cardDiv = document.createElement("div");

        cardDiv.className = "card";

        const titleElem = document.createElement("h3");

        titleElem.textContent = announcement.title;

        const bodyElem = document.createElement("p");

        bodyElem.textContent = announcement.body;

        cardDiv.appendChild(titleElem);

        cardDiv.appendChild(bodyElem);

        latestDiv.appendChild(cardDiv);

    });

}



function renderTimetable() {

    const tableBody =
        document.querySelector("#timetable tbody") ||
        document.getElementById("timetable");

    if (!tableBody) {
        return;
    }

    let target;

    if (tableBody.tagName.toLowerCase() === "table") {

        target =
            tableBody.getElementsByTagName("tbody")[0] ||
            tableBody;

    } else {

        target = tableBody;

    }

    target.innerHTML = "";

    timetable.forEach(function (entry) {

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${entry.activity}</td>
            <td>${entry.day}</td>
            <td>${entry.time}</td>
            <td>${entry.hall}</td>
        `;

        target.appendChild(row);

    });

}



document.addEventListener("DOMContentLoaded", function () {




    const registerForm =
        document.getElementById("registerForm");


    if (registerForm) {

        registerForm.addEventListener(
            "submit",
            async function (e) {

                e.preventDefault();

                const formData =
                    new FormData(registerForm);


                console.log(
                    "📤 إرسال بيانات التسجيل إلى Flask..."
                );


                try {

                    const response = await fetch(
                        registerForm.action,
                        {
                            method: "POST",
                            body: formData
                        }
                    );


                    const result =
                        await response.text();


                    if (response.ok) {

                        alert(result);


                        registerForm.reset();


                        const course =
                            document.getElementById("course");


                        if (course) {

                            course.innerHTML =
                                '<option value="" selected disabled>اختر الحلقة أولاً</option>';

                        }

                    } else {

                        console.error(
                            "❌ Server Error:",
                            result
                        );

                        alert(
                            "حدث خطأ أثناء التسجيل."
                        );

                    }


                } catch (error) {

                    console.error(
                        "❌ Connection Error:",
                        error
                    );

                    alert(
                        "تعذر الاتصال بالسيرفر! تأكدي أن Flask شغال."
                    );

                }

            }
        );

    }




    const ayahElem =
        document.getElementById("ayah");


    if (ayahElem) {

        const randomAyah =
            Math.floor(
                Math.random() * ayat.length
            );

        ayahElem.textContent =
            ayat[randomAyah];

    }


    const hadithElem =
        document.getElementById("hadith");


    if (hadithElem) {

        const randomHadith =
            Math.floor(
                Math.random() * ahadith.length
            );

        hadithElem.textContent =
            "قال رسول الله ﷺ: " +
            ahadith[randomHadith];

    }



    renderAnnouncements();


    renderTimetable();



    const category =
        document.getElementById("category");


    const course =
        document.getElementById("course");


    if (category && course) {

        category.addEventListener(
            "change",
            function () {

                course.innerHTML =
                    '<option value="" selected disabled>اختر الحلقة</option>';


                const selected =
                    category.value;


                if (
                    selected &&
                    courses[selected]
                ) {

                    courses[selected].forEach(
                        function (item) {

                            const option =
                                document.createElement(
                                    "option"
                                );


                            option.textContent =
                                item;


                            option.value =
                                item;


                            course.appendChild(
                                option
                            );

                        }
                    );

                }

            }
        );

    }

});

