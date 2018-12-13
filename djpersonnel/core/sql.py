LEVEL3 = '''
SELECT
    trim(id_rec.lastname) as lastname, trim(id_rec.firstname) as firstname,
    id_rec.id, trim(job_rec.descr) as description, trim(job_rec.job_title) as job_title,
    trim(email_rec.line1) as email,
    job_rec.tpos_no
FROM
    id_rec
LEFT JOIN
    job_rec
ON
    id_rec.id = job_rec.id
LEFT JOIN
    aa_rec as email_rec
ON
    (id_rec.id = email_rec.id AND email_rec.aa = "EML1")
WHERE
    job_rec.tpos_no IN (
        2674,2872,2876,2902,3200,3238,3254,3561,3587,3644,3374,3375,3376
    )
AND
    job_rec.end_date IS NULL
ORDER BY
    id_rec.lastname
'''
