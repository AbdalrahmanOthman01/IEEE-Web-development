const mysql = require("mysql2");

// ==========================================
// إعداد الـ Pool الرئيسي
// ==========================================

const pool = mysql.createPool({
    host: "127.0.0.1",
    port: 3306,
    user: "root",
    password: "WJ28@krhps",
    database: "telwani_db",

    // مهم جدًا لظهور العربي بشكل صحيح
    charset: "utf8mb4",

    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
});


// ==========================================
// تهيئة قاعدة البيانات
// ==========================================

const initDatabase = () => {

    const setupConn = mysql.createConnection({
        host: "127.0.0.1",
        port: 3306,
        user: "root",
        password: "WJ28@krhps",

        // مهم جدًا
        charset: "utf8mb4"
    });


    setupConn.connect((err) => {

        if (err) {
            console.error(
                "❌ فشل الاتصال بالسيرفر لتأسيس الداتابيز:",
                err.message
            );
            return;
        }


        // ==========================================
        // إنشاء قاعدة البيانات
        // ==========================================

        setupConn.query(
            `CREATE DATABASE IF NOT EXISTS telwani_db
             CHARACTER SET utf8mb4
             COLLATE utf8mb4_unicode_ci`,
            (err) => {

                if (err) {

                    console.error(
                        "❌ خطأ في إنشاء الداتابيز:",
                        err.message
                    );

                    setupConn.end();
                    return;
                }


                // ==========================================
                // اختيار قاعدة البيانات
                // ==========================================

                setupConn.changeUser(
                    {
                        database: "telwani_db",
                        charset: "utf8mb4"
                    },
                    (err) => {

                        if (err) {

                            console.error(
                                "❌ خطأ في اختيار قاعدة البيانات:",
                                err.message
                            );

                            setupConn.end();
                            return;
                        }


                        // ==========================================
                        // جدول التسجيلات
                        // ==========================================

                        const createRegistrationsTableSql = `
                            CREATE TABLE IF NOT EXISTS registrations (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                fullName VARCHAR(255) NOT NULL,
                                age INT,
                                gender VARCHAR(10),
                                phone VARCHAR(20) NOT NULL,
                                email VARCHAR(255),
                                course VARCHAR(255),
                                way VARCHAR(50),
                                halaqa VARCHAR(255),
                                level VARCHAR(255),
                                day VARCHAR(255),
                                notes TEXT,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )
                        `;


                        // ==========================================
                        // جدول الأسئلة
                        // ==========================================

                        const createQuestionsTableSql = `
                            CREATE TABLE IF NOT EXISTS questions (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                question TEXT NOT NULL,
                                answer TEXT DEFAULT NULL,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )
                        `;


                        // ==========================================
                        // إنشاء جدول التسجيلات
                        // ==========================================

                        setupConn.query(
                            createRegistrationsTableSql,
                            (err) => {

                                if (err) {

                                    console.error(
                                        "❌ خطأ في إنشاء جدول registrations:",
                                        err.message
                                    );

                                } else {

                                    console.log(
                                        "✅ جدول registrations جاهز."
                                    );
                                }


                                // ==========================================
                                // إنشاء جدول الأسئلة
                                // ==========================================

                                setupConn.query(
                                    createQuestionsTableSql,
                                    (err) => {

                                        if (err) {

                                            console.error(
                                                "❌ خطأ في إنشاء جدول questions:",
                                                err.message
                                            );

                                        } else {

                                            console.log(
                                                "✅ جدول questions جاهز بنجاح!"
                                            );
                                        }


                                        setupConn.end();

                                    }
                                );

                            }
                        );

                    }
                );

            }
        );

    });

};


// تشغيل التهيئة
initDatabase();


// تصدير الـ Pool
module.exports = pool;

