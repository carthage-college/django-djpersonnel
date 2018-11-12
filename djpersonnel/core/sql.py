LEVEL3 = '''
SELECT
    id_rec.lastname, id_rec.firstname,
    id_rec.id, job_rec.descr, job_rec.job_title,
    email_rec.line1 as email,
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
        2483,2485,2872,2874,2876,2877,2930,3200,3238,3566,3587,3644
    )
AND
    job_rec.end_date IS NULL
ORDER BY
    id_rec.lastname
'''
